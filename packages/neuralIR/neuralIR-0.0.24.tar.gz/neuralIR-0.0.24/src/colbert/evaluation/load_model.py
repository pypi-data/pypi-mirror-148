import os
import ujson
import torch
import random

from collections import defaultdict, OrderedDict

from colbert.parameters import DEVICE
from colbert.modeling.factory import get_colbert_from_pretrained
from colbert.utils.utils import print_message, load_checkpoint


def load_model(args, do_print=True):
    if args.model_type == 'tinybert':
        colbert = get_colbert_from_pretrained(args.model_type, # eg 'bert-base-uncased'
                                              query_maxlen=args.query_maxlen,
                                              doc_maxlen=args.doc_maxlen,
                                              dim=args.dim,
                                              similarity_metric=args.similarity,
                                              mask_punctuation=args.mask_punctuation,
                                              local_models_repository=args.local_models_repository)
    else:
        colbert = get_colbert_from_pretrained(args.model_type, # eg 'bert-base-uncased'
                                          query_maxlen=args.query_maxlen,
                                          doc_maxlen=args.doc_maxlen,
                                          dim=args.dim,
                                          similarity_metric=args.similarity,
                                          mask_punctuation=args.mask_punctuation)

    colbert = colbert.to(DEVICE)

    print_message("#> Loading model checkpoint.", condition=do_print)

    checkpoint = load_checkpoint(args.checkpoint, colbert, do_print=do_print)

    colbert.eval()

    return colbert, checkpoint
