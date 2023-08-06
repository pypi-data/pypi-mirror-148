import torch

from transformers import BertTokenizerFast
from colbert.modeling.tokenization.utils import _split_into_batches


class QueryTokenizerMBERT():
    def __init__(self, query_maxlen, model_type='bert-base-multilingual-uncased'):
        self.tok = BertTokenizerFast.from_pretrained(model_type)
        print("Using Tokenizer", model_type, "Vocab size", self.tok.vocab_size)
        self.query_maxlen = query_maxlen

        self.Q_marker_token, self.Q_marker_token_id = '[Q]', self.tok.convert_tokens_to_ids('[unused1]')
        self.cls_token, self.cls_token_id = self.tok.cls_token, self.tok.cls_token_id
        self.sep_token, self.sep_token_id = self.tok.sep_token, self.tok.sep_token_id
        self.mask_token, self.mask_token_id = self.tok.mask_token, self.tok.mask_token_id

        assert self.Q_marker_token_id == 1 and self.mask_token_id == 103

    def tokenize(self, batch_text, add_special_tokens=False):
        assert type(batch_text) in [list, tuple], (type(batch_text))

        tokens = [self.tok.tokenize(x, add_special_tokens=False) for x in batch_text]

        if not add_special_tokens:
            return tokens

        prefix, suffix = [self.cls_token, self.Q_marker_token], [self.sep_token]
        tokens = [prefix + lst + suffix + [self.mask_token] * (self.query_maxlen - (len(lst)+3)) for lst in tokens]

        return tokens

    def encode(self, batch_text, add_special_tokens=False):
        assert type(batch_text) in [list, tuple], (type(batch_text))

        ids = self.tok(batch_text, add_special_tokens=False)['input_ids']

        if not add_special_tokens:
            return ids

        prefix, suffix = [self.cls_token_id, self.Q_marker_token_id], [self.sep_token_id]
        ids = [prefix + lst + suffix + [self.mask_token_id] * (self.query_maxlen - (len(lst)+3)) for lst in ids]

        return ids

    def tensorize(self, batch_text, bsize=None):
        assert type(batch_text) in [list, tuple], (type(batch_text))

        # add placehold for the [Q] marker
        batch_text = ['. ' + x for x in batch_text]

        obj = self.tok(batch_text, padding='max_length', truncation=True,
                       return_tensors='pt', max_length=self.query_maxlen)

        ids, mask = obj['input_ids'], obj['attention_mask']

        # postprocess for the [Q] marker and the [MASK] augmentation
        ids[:, 1] = self.Q_marker_token_id
        ids[ids == 0] = self.mask_token_id

        if bsize:
            batches = _split_into_batches(ids, mask, bsize)
            return batches

        return ids, mask


### bert-base-multilingual-cased
# In [1]:  from colbert.modeling.tokenization import QueryTokenizerMBERT

# In [2]:  t=QueryTokenizerMBERT(50)
#Using Tokenizer bert-base-multilingual-cased Vocab size 119547
# In [3]:  t.tensorize(['what is the answer?', 'is that not completely ridiculously false?'])
# Out[3]:
# (tensor([[  101,     1, 12976, 10124, 10105, 57085,   136,   102,   103,   103,
#             103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#             103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#             103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#             103,   103,   103,   103,   103,   103,   103,   103,   103,   103],
#          [  101,     1, 10124, 10189, 10472, 27185, 29956, 55170, 22540, 61289,
#           37155,   136,   102,   103,   103,   103,   103,   103,   103,   103,
#             103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#             103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#             103,   103,   103,   103,   103,   103,   103,   103,   103,   103]]),
#  tensor([[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0],
#          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0]]))

# In [4]: t.Q_marker_token_id
# Out[4]: 1

# In [5]:  t.mask_token_id
# Out[5]: 103

# In [6]:  t.cls_token_id
# Out[6]: 101

# In [7]: t.sep_token_id
# Out[7]: 102

### bert-base-multilingual-uncased

# from colbert.modeling.tokenization import QueryTokenizerMBERT
# >>> t=QueryTokenizerMBERT(50)
# Using Tokenizer bert-base-multilingual-uncased Vocab sizeL 105879
# >>> t.tensorize(['what is the answer?', 'is that not completely ridiculously false?'])
# (tensor([[  101,     1, 11523, 10127, 10103, 42942,   136,   102,   103,   103,
#            103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#            103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#            103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#            103,   103,   103,   103,   103,   103,   103,   103,   103,   103],
#         [  101,     1, 10127, 10203, 10497, 26785, 89215, 21131, 34238, 38052,
#          10158, 30368,   136,   102,   103,   103,   103,   103,   103,   103,
#            103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#            103,   103,   103,   103,   103,   103,   103,   103,   103,   103,
#            103,   103,   103,   103,   103,   103,   103,   103,   103,   103]]), tensor([[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0]]))
# >>> t.Q_marker_token_id
# 1
# >>> t.mask_token_id
# 103
# >>> t.cls_token_id
# 101
# >>> t.sep_token_id
# 102

