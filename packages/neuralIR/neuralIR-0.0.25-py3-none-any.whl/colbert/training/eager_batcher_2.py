import random

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
        self.position = 0

        triples_path = args.triples if explicit_triples_path is None else explicit_triples_path
        self.triples = self._load_triples(triples_path, rank, nranks)
        self.reader = open(args.triples, mode='r', encoding="utf-8")
        self.length = len(self.reader.readlines())

    def shuffle(self):
        print_message("#> Shuffling triples...")
        random.shuffle(self.triples)

    def _load_triples(self, path, rank, nranks):
        """
        NOTE: For distributed sampling, this isn't equivalent to perfectly uniform sampling.
        In particular, each subset is perfectly represented in every batch! However, since we never
        repeat passes over the data, we never repeat any particular triple, and the split across
        nodes is random (since the underlying file is pre-shuffled), there's no concern here.
        """
        print_message("#> Loading triples...")

        triples = []

        with open(path) as f:
            for line_idx, line in enumerate(f):
                if line_idx % nranks == rank:
                    query, pos, neg = line.strip().split('\t')
                    triples.append((query, pos, neg))

        return triples

    def __iter__(self):
        return self

    def __len__(self):
        return self.length

    def __next__(self):
        queries, positives, negatives = [], [], []

        for line_idx in range(self.bsize * self.nranks):
            if (self.position + line_idx) % self.nranks != self.rank:
                continue

            real_line_idx = (self.position + line_idx) % len(self.triples)
            query, pos, neg = self.triples[real_line_idx]

            queries.append(query)
            positives.append(pos)
            negatives.append(neg)

        self.position += line_idx + 1

        return self.collate(queries, positives, negatives)

    def collate(self, queries, positives, negatives):
        assert len(queries) == len(positives) == len(negatives) == self.bsize

        return self.tensorize_triples(queries, positives, negatives, self.bsize // self.accumsteps)

    def skip_to_batch(self, batch_idx, intended_batch_size):
        Run.warn(f'Skipping to batch #{batch_idx} (with intended_batch_size = {intended_batch_size}) for training.')
        self.position = intended_batch_size * batch_idx
