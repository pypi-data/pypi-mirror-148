import os
import ujson

from functools import partial
from colbert.utils.utils import print_message
from colbert.modeling.tokenization import tensorize_triples
from colbert.modeling.factory import get_query_tokenizer, get_doc_tokenizer

from colbert.utils.runs import Run


class EagerBatcher():
    def __init__(self, args, rank=0, nranks=1, explicit_triples_path=None, is_teacher=False):
        self.rank, self.nranks = rank, nranks
        self.bsize, self.accumsteps = args.bsize, args.accumsteps

        self.query_tokenizer = get_query_tokenizer(args.model_type if (not is_teacher or args.teacher_model_type is None) else args.teacher_model_type, args.query_maxlen)
        self.doc_tokenizer = get_doc_tokenizer(args.model_type if (not is_teacher or args.teacher_model_type is None) else args.teacher_model_type, args.doc_maxlen if not is_teacher else args.teacher_doc_maxlen)
        self.tensorize_triples = partial(tensorize_triples, self.query_tokenizer, self.doc_tokenizer)

        self.triples_path = args.triples if explicit_triples_path is None else explicit_triples_path
        self._reset_triples()

    def _reset_triples(self):
        self.reader = open(self.triples_path, mode='r', encoding="utf-8")
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        queries, positives, negatives = [], [], []

        line_idx = -1

        for line_idx, line in zip(range(self.bsize * self.nranks), self.reader):
            if (self.position + line_idx) % self.nranks != self.rank:
                continue
            query, pos, neg = line.strip().split('\t')

            queries.append(query)
            positives.append(pos)
            negatives.append(neg)

        self.position += line_idx + 1

        if len(queries) < self.bsize:
            raise StopIteration

        return self.collate(queries, positives, negatives)

    def collate(self, queries, positives, negatives):
        assert len(queries) == len(positives) == len(negatives) == self.bsize

        return self.tensorize_triples(queries, positives, negatives, self.bsize // self.accumsteps)

    def skip_to_batch(self, batch_idx, intended_batch_size):
        self._reset_triples()

        Run.warn(f'Skipping to batch #{batch_idx} (with intended_batch_size = {intended_batch_size}) for training.')

        _ = [self.reader.readline() for _ in range(batch_idx * intended_batch_size)]

        return None
