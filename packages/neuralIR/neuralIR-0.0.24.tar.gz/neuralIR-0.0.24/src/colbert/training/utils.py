import os
import math
import torch

from colbert.utils.runs import Run
from colbert.utils.utils import print_message, save_checkpoint
from colbert.parameters import SAVED_CHECKPOINTS


def print_progress(scores):
    positive_avg, negative_avg = round(scores[:, 0].mean().item(), 2), round(scores[:, 1].mean().item(), 2)
    print("#>>>   ", positive_avg, negative_avg, '\t\t|\t\t', positive_avg - negative_avg)


def manage_checkpoints(args, colbert, optimizer, amp, batch_idx, num_per_epoch, epoch_idx=0):
    arguments = args.input_arguments.__dict__

    saved_name = ""
    path = os.path.join(Run.path, 'checkpoints')

    if not os.path.exists(path):
        os.mkdir(path)
    prefix = os.path.join(path, "colbert.dnn")

    if args.save_epochs == -1:
        if batch_idx % args.save_steps == 0:
            saved_name = prefix + f".batch_{batch_idx}.model"
            save_checkpoint(saved_name, epoch_idx, batch_idx, colbert, optimizer, amp, arguments)
    else:
        if batch_idx * args.bsize * args.nranks % int(args.save_epochs * num_per_epoch) < args.bsize * args.nranks:
            if args.save_epochs.is_integer():
                saved_name = prefix + f".epoch_{epoch_idx}.model"
            else:
                saved_name = prefix + f".epoch_{epoch_idx}_batch_{batch_idx}.model"

            save_checkpoint(saved_name, epoch_idx, batch_idx, colbert, optimizer, amp, arguments)

    if batch_idx in SAVED_CHECKPOINTS or batch_idx == args.maxsteps:
        name = prefix + f".batch_{batch_idx}.model"
        if not name == saved_name:
            save_checkpoint(name, epoch_idx, batch_idx, colbert, optimizer, amp, arguments)

    if (batch_idx * args.bsize * args.nranks) % (args.epochs * num_per_epoch) < args.bsize * args.nranks:
        name = prefix + f".epoch_{args.epochs - 1}.model"
        if not name == saved_name:
            save_checkpoint(name, epoch_idx, batch_idx, colbert, optimizer, amp, arguments)
