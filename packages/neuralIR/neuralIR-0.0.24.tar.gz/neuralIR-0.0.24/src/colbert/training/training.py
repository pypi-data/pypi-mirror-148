import enum
import os
import errno
import math
import random
import sys
import glob
import time
from queue import Empty

import torch
import torch.nn as nn
import numpy as np
from scipy import spatial
import copy
import time

from transformers import AdamW
from colbert.utils.runs import Run
from colbert.utils.amp import MixedPrecisionManager

from colbert.training.lazy_batcher import LazyBatcher
from colbert.training.eager_batcher_2 import EagerBatcher
from colbert.parameters import DEVICE

from colbert.modeling.factory import get_colbert_from_pretrained
from colbert.utils import signals
from colbert.utils.utils import batch, print_message, save_checkpoint
from colbert.training.utils import print_progress, manage_checkpoints

from colbert.utils.runs import Run

from transformers import XLMRobertaModel, XLMRobertaTokenizer, BertPreTrainedModel

def cycle(reader):
    ''' repeat all items from the generator forever ...
    I could maybe(?) use itertools.cycle() here, 
    but I want to ensure the call to _reset_triples()'''
    while True:
        yield from reader
        reader._reset_triples()

def calculate_distance(student_out, teacher_out):
    '''calculate the distance between student output tokens and
    teacher output tokens'''
    # start = time.time()
    prod = teacher_out.matmul(student_out.transpose(1, 2))
    student_out_norm = torch.norm(student_out, p=2, dim=-1)
    teacher_out_norm = torch.norm(teacher_out, p=2, dim=-1)
    m = teacher_out_norm.unsqueeze(2) * student_out_norm.unsqueeze(1)
    esp = torch.ones_like(m) * 10**-8
    distance = torch.ones_like(m) - prod /(m + esp)
    # end = time.time()
    # print("time to calculation distance matrix: ", end - start)
    return distance

def save_distance_matrix(colbert, batch_student_out, batch_teacher_out, batch_student_queries, batch_teacher_queries, file_name):
    '''Debug purpose'''
    tokenizer = colbert.tokenizer.from_pretrained('xlm-roberta-base')
    with open(file_name , "w") as f:
        batch_distance = calculate_distance(batch_student_out, batch_teacher_out)
        for distance, student_ids, teacher_ids in zip(batch_distance, batch_student_queries[0], batch_teacher_queries[0]):
            student_tokens = tokenizer.convert_ids_to_tokens(student_ids)
            teacher_tokens = tokenizer.convert_ids_to_tokens(teacher_ids)
            tokenList = '## ' + ' '.join([str(st) for st in student_tokens])
            f.write(tokenList)
            f.write('\n')
            for tt, dis in zip(teacher_tokens, distance):
                disList = ' '.join([str(elem.item()) for elem in dis])
                disList = str(tt) + ' ' + disList
                f.write(disList)
                f.write('\n')

def align(maxlen, student_out, teacher_out, teacher_queries):
    '''re-order teacher output tokens so that it aligns with
    student output tokens with greedy search'''
    batch_distance_array=calculate_distance(student_out, teacher_out)
    batch_distance_array = batch_distance_array.cpu().detach().numpy()
    for idx, distance_array in enumerate(batch_distance_array):
        swaps = []
        for i in range(maxlen):
            minValue =np.amin(distance_array)
            indexs = np.where(distance_array == np.amin(minValue))
            #get the index of the first min value
            i, j = indexs[0][0], indexs[1][0]
            #swap arrary row i and row j
            distance_array[[i, j]] = distance_array[[j, i]]
            distance_array[j, :] = 10  #anything larger than 1 to avoid double count
            distance_array[:, j] = 10
            swaps.append((i,j))
        for swap in swaps:
            teacher_out[idx][[swap[0], swap[1]]] = teacher_out[idx][[swap[1], swap[0]]]
            teacher_queries[0][idx][[swap[0], swap[1]]] = teacher_queries[0][idx][[swap[1], swap[0]]]

def train(args):
    random.seed(12345)
    np.random.seed(12345)
    torch.manual_seed(12345)
    torch.cuda.manual_seed(12345)
    if args.distributed:
        torch.cuda.manual_seed_all(12345)

    if args.distributed:
        assert args.bsize % args.nranks == 0, (args.bsize, args.nranks)
        assert args.accumsteps == 1
        args.bsize = args.bsize // args.nranks

        print("Using args.bsize =", args.bsize, "(per process) and args.accumsteps =", args.accumsteps)

    if args.lazy:
        reader = LazyBatcher(args, (0 if args.rank == -1 else args.rank), args.nranks)
    else:
        reader = EagerBatcher(args, (0 if args.rank == -1 else args.rank), args.nranks, args.triples, False)
        if args.teacher_checkpoint is not None:
            teacher_reader = EagerBatcher(args, (0 if args.rank == -1 else args.rank), args.nranks, args.teacher_triples, True)

    if args.rank not in [-1, 0]:
        torch.distributed.barrier()

    colbert = get_colbert_from_pretrained(args.model_type, # eg 'bert-base-uncased',
                                          query_maxlen=args.query_maxlen,
                                          doc_maxlen=args.doc_maxlen,
                                          dim=args.dim,
                                          similarity_metric=args.similarity,
                                          mask_punctuation=args.mask_punctuation,
                                          local_models_repository=args.local_models_repository,
                                          distill_query_passage_separately = args.distill_query_passage_separately,
                                          query_only = args.query_only,
                                          )

    if args.teacher_checkpoint is not None:
          teacher_colbert = get_colbert_from_pretrained(args.teacher_model_type if args.teacher_model_type is not None else args.model_type, # eg 'bert-base-uncased',
                                      query_maxlen=args.query_maxlen,
                                      doc_maxlen=args.teacher_doc_maxlen,
                                      dim=args.dim,
                                      similarity_metric=args.similarity,
                                      distill_query_passage_separately = args.distill_query_passage_separately,
                                      query_only = args.query_only,
                                      mask_punctuation=args.mask_punctuation,
                                      )

    if args.init_from_lm is not None and args.checkpoint is None:  
        # checkpoint should override init_from_lm since it continues an already init'd run
        lmweights=torch.load(args.init_from_lm) # expect path to pytorch_model.bin
        # fix differences in keys - we could use strict=False in load_state_dict, but prefer to expose the differences
        lmweights['linear.weight']=colbert.linear.weight
        # we don't need the keys in the lm head
        keys_to_drop= ['lm_head.dense.weight', 'lm_head.dense.bias', 'lm_head.layer_norm.weight', 'lm_head.layer_norm.bias', 'lm_head.decoder.weight', 'lm_head.decoder.bias', 'lm_head.bias']
        if args.model_type=='xlm-roberta-base':
            # TODO other model types may have a few extra keys to handle also ...
            lmweights['roberta.pooler.dense.weight']=colbert.roberta.pooler.dense.weight
            lmweights['roberta.pooler.dense.bias']=colbert.roberta.pooler.dense.bias
            # I don't know what roberta.embeddings.position_ids is but it doesn't seem to be part of the model ...
            keys_to_drop += ['roberta.embeddings.position_ids']
        elif args.model_type == 'tinybert':
            keys_to_drop = [ "cls.predictions.bias", "cls.predictions.transform.dense.weight", "cls.predictions.transform.dense.bias", "cls.predictions.transform.LayerNorm.weight", "cls.predictions.transform.LayerNorm.bias", "cls.predictions.decoder.weight", "cls.seq_relationship.weight", "cls.seq_relationship.bias", "fit_denses.0.weight", "fit_denses.0.bias", "fit_denses.1.weight", "fit_denses.1.bias", "fit_denses.2.weight", "fit_denses.2.bias", "fit_denses.3.weight", "fit_denses.3.bias", "fit_denses.4.weight", "fit_denses.4.bias"]

        for k in keys_to_drop:
            lmweights.pop(k)

        colbert.load_state_dict(lmweights)

    if args.checkpoint is not None:
        print_message(f"#> Starting from checkpoint {args.checkpoint}")
        checkpoint = torch.load(args.checkpoint, map_location='cpu')

        try:
            colbert.load_state_dict(checkpoint['model_state_dict'])
        except:
            print_message("[WARNING] Loading checkpoint with strict=False")
            colbert.load_state_dict(checkpoint['model_state_dict'], strict=False)

    if args.teacher_checkpoint is not None:
        print_message(f"#> Loading teacher model from checkpoint {args.teacher_checkpoint}")
        teacher_checkpoint = torch.load(args.teacher_checkpoint, map_location='cpu')

        try:
            teacher_colbert.load_state_dict(teacher_checkpoint['model_state_dict'])
        except:
            print_message("[WARNING] Loading teacher checkpoint with strict=False")
            teacher_colbert.load_state_dict(teacher_checkpoint['model_state_dict'], strict=False)

    if args.rank == 0:
        torch.distributed.barrier()

    colbert = colbert.to(DEVICE)
    colbert.train()

    if args.teacher_checkpoint is not None:
        teacher_colbert = teacher_colbert.to(DEVICE)
        if args.distill_query_passage_separately:
            if args.loss_function == 'MSE':
                student_teacher_loss_fct = torch.nn.MSELoss()
            elif args.loss_function == 'l1':
                student_teacher_loss_fct = torch.nn.L1Loss()
        else:
            student_teacher_loss_fct = torch.nn.KLDivLoss(reduction="batchmean")  # or MSE?

    if args.distributed:
        colbert = torch.nn.parallel.DistributedDataParallel(colbert, device_ids=[args.rank],
                                                            output_device=args.rank,
                                                            find_unused_parameters=True)
        if args.teacher_checkpoint is not None:
            teacher_colbert = torch.nn.parallel.DistributedDataParallel(teacher_colbert, device_ids=[args.rank],
                                                                output_device=args.rank,
                                                                find_unused_parameters=True)

    optimizer = AdamW(filter(lambda p: p.requires_grad, colbert.parameters()), lr=args.lr, eps=1e-8)
    optimizer.zero_grad()
    if args.resume_optimizer:
        print_message(f"#> Resuming optimizer from checkpoint {args.checkpoint}")
        torch.set_rng_state(checkpoint['torch_rng_state'].to(torch.get_rng_state().device))
        torch.cuda.set_rng_state_all([ state.to(torch.cuda.get_rng_state_all()[pos].device) for pos, state in enumerate(checkpoint['torch_cuda_rng_states']) ] )
        np.random.set_state(checkpoint['np_rng_state'])
        random.setstate(checkpoint['python_rng_state'])

        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    amp = MixedPrecisionManager(args.amp)
    if args.resume_optimizer and args.amp:
        amp.scaler.load_state_dict(checkpoint['scaler_state_dict'])

    criterion = nn.CrossEntropyLoss()
    labels = torch.zeros(args.bsize, dtype=torch.long, device=DEVICE)

    start_time = time.time()
    train_loss = 0.0

    start_batch_idx = 0

    if args.resume:
        assert args.checkpoint is not None
        start_batch_idx = checkpoint['batch']

        reader.skip_to_batch(start_batch_idx, checkpoint['arguments']['bsize'])
        if args.teacher_checkpoint is not None:
            teacher_reader.skip_to_batch(start_batch_idx, checkpoint['arguments']['bsize'])

    maxsteps = min(args.maxsteps, math.ceil((args.epochs * len(reader)) / (args.bsize * args.nranks)))
    path = os.path.join(Run.path, 'checkpoints')
    name = os.path.join(path, "colbert-EXIT.dnn")
    arguments = args.input_arguments.__dict__
    exit_queue = signals.checkpoint_on_exit(args.rank)
    Run.info(f"maxsteps: {args.maxsteps}")
    Run.info(f"{args.epochs} epochs of {len(reader)} examples")
    Run.info(f"batch size: {args.bsize}")
    Run.info(f"maxsteps set to {maxsteps}")
    print_every_step = False

    if args.teacher_checkpoint is not None:
        for batch_idx, BatchSteps, teacher_BatchSteps in zip(range(start_batch_idx, maxsteps), reader, teacher_reader):
            n_instances = batch_idx * args.bsize * args.nranks
            if (n_instances + 1) % len(reader) < args.bsize * args.nranks:
                Run.info("====== Epoch {}...".format((n_instances+1) // len(reader)))
                if args.shuffle_every_epoch:
                    print_message("[WARNING] Data shuffling is not supported for Student/Teacher training")
                    #Run.info("Shuffling ...")
                    #reader.shuffle()
                else:
                    Run.info("Shuffling not specified.")
            if batch_idx % 100 == 0:
                Run.info(f"Batch {batch_idx}")

            this_batch_loss = 0.0

            for queries_passages, teacher_queries_passages in zip(BatchSteps, teacher_BatchSteps):
                assert(args.teacher_model_type is not None or torch.equal(queries_passages[1][0], teacher_queries_passages[1][0]))

                with amp.context():
                    if args.distill_query_passage_separately :
                        if args.query_only:
                            print("training with query only")
                            with torch.no_grad():
                                teacher_output_q = teacher_colbert(teacher_queries_passages[0], teacher_queries_passages[1])
                            student_output_q = colbert(queries_passages[0], queries_passages[1])
                            teacher_queries = copy.deepcopy(teacher_queries_passages[0])
                            student_queries = copy.deepcopy(queries_passages[0])
                            maxlen = args.query_maxlen
                            # save_distance_matrix(colbert, student_output_q, teacher_output_q, student_queries, teacher_queries, 'before_alignment.txt')
                            align(maxlen, student_output_q, teacher_output_q, teacher_queries)
                            # save_distance_matrix(colbert, student_output_q, teacher_output_q, student_queries, teacher_queries, 'after_alignment.txt')
                            loss = student_teacher_loss_fct(student_output_q, teacher_output_q)
                        else:
                            with torch.no_grad():
                                teacher_scores, teacher_output_q, teacher_output_p  = teacher_colbert(teacher_queries_passages[0], teacher_queries_passages[1])
                            scores, student_output_q, student_output_p = colbert(queries_passages[0], queries_passages[1])
                            teacher_queries = copy.deepcopy(teacher_queries_passages[0])
                            maxlen = args.query_maxlen
                            align(maxlen, student_output_q, teacher_output_q, teacher_queries)
                            loss = args.query_weight * student_teacher_loss_fct(student_output_q, teacher_output_q) + (1- args.query_weight)*student_teacher_loss_fct(student_output_p, teacher_output_p)
                    else:
                        scores = colbert(queries_passages[0], queries_passages[1]).view(2, -1).permute(1, 0)

                        with torch.no_grad():
                            teacher_scores = teacher_colbert(teacher_queries_passages[0], teacher_queries_passages[1]).view(2, -1).permute(1, 0)

                        loss = student_teacher_loss_fct(
                                    torch.nn.functional.log_softmax(scores / args.student_teacher_temperature, dim=-1),
                                    torch.nn.functional.softmax(teacher_scores / args.student_teacher_temperature, dim=-1),
                                ) * (args.student_teacher_temperature ** 2)

                    loss = loss / args.accumsteps

                if args.rank < 1 and print_every_step:
                    if args.distill_query_passage_separately:
                        print("loss: ", loss.item())
                    else:
                        print_progress(scores)

                amp.backward(loss)

                train_loss += loss.item()
                this_batch_loss += loss.item()

            amp.step(colbert, optimizer)

            if args.rank < 1:
                avg_loss = train_loss / (batch_idx+1)

                num_examples_seen = (batch_idx - start_batch_idx) * args.bsize * args.nranks
                elapsed = float(time.time() - start_time)

                log_to_mlflow = (batch_idx % 20 == 0)
                Run.log_metric('train/avg_loss', avg_loss, step=batch_idx, log_to_mlflow=log_to_mlflow)
                Run.log_metric('train/batch_loss', this_batch_loss, step=batch_idx, log_to_mlflow=log_to_mlflow)
                Run.log_metric('train/examples', num_examples_seen, step=batch_idx, log_to_mlflow=log_to_mlflow)
                Run.log_metric('train/throughput', num_examples_seen / elapsed, step=batch_idx, log_to_mlflow=log_to_mlflow)

                num_per_epoch = len(reader)
                epoch_idx = ((batch_idx + 1) * args.bsize * args.nranks) // num_per_epoch - 1
                print_message(batch_idx, avg_loss)
                try:
                    exit_queue.get_nowait()
                    save_checkpoint(name, epoch_idx, batch_idx, colbert, optimizer, amp, arguments)
                    sys.exit(0)
                except Empty:
                    manage_checkpoints(args, colbert, optimizer, amp, batch_idx + 1, num_per_epoch, epoch_idx)
    else:
       for batch_idx, BatchSteps in zip(range(start_batch_idx, maxsteps), reader):
            n_instances = batch_idx * args.bsize * args.nranks
            if (n_instances + 1) % len(reader) < args.bsize * args.nranks:
                Run.info("====== Epoch {}...".format((n_instances+1) // len(reader)))
                if args.shuffle_every_epoch:
                    Run.info("Shuffling ...")
                    reader.shuffle()
                else:
                    Run.info("Shuffling not specified.")
            if batch_idx % 100 == 0:
                Run.info(f"Batch {batch_idx}")
            this_batch_loss = 0.0
            for queries, passages in BatchSteps:
                with amp.context():
                    scores = colbert(queries, passages).view(2, -1).permute(1, 0)
                    loss = criterion(scores, labels[:scores.size(0)])
                    loss = loss / args.accumsteps

                if args.rank < 1 and print_every_step:
                    print_progress(scores)

                amp.backward(loss)

                train_loss += loss.item()
                this_batch_loss += loss.item()

            amp.step(colbert, optimizer)

            if args.rank < 1:
                avg_loss = train_loss / (batch_idx+1)

                num_examples_seen = (batch_idx - start_batch_idx) * args.bsize * args.nranks
                elapsed = float(time.time() - start_time)

                log_to_mlflow = (batch_idx % 20 == 0)
                Run.log_metric('train/avg_loss', avg_loss, step=batch_idx, log_to_mlflow=log_to_mlflow)
                Run.log_metric('train/batch_loss', this_batch_loss, step=batch_idx, log_to_mlflow=log_to_mlflow)
                Run.log_metric('train/examples', num_examples_seen, step=batch_idx, log_to_mlflow=log_to_mlflow)
                Run.log_metric('train/throughput', num_examples_seen / elapsed, step=batch_idx, log_to_mlflow=log_to_mlflow)

                num_per_epoch = len(reader)
                epoch_idx = ((batch_idx + 1) * args.bsize * args.nranks) // num_per_epoch - 1
                print_message(batch_idx, avg_loss)
                try:
                    exit_queue.get_nowait()
                    save_checkpoint(name, epoch_idx, batch_idx, colbert, optimizer, amp, arguments)
                    sys.exit(0)
                except Empty:
                    manage_checkpoints(args, colbert, optimizer, amp, batch_idx + 1, num_per_epoch, epoch_idx)


    name = os.path.join(path, "colbert-LAST.dnn")
    list_of_files = glob.glob(f'{path}/*.model')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    Run.info(f"Make a sym link of {latest_file} to {name}")
    try:
        os.symlink(latest_file, name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(name)
            os.symlink(latest_file, name)
        else:
            raise
