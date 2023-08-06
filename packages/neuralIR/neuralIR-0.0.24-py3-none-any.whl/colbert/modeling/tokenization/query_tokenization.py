import torch

from transformers import BertTokenizerFast
from colbert.modeling.tokenization.utils import _split_into_batches


class QueryTokenizer():
    def __init__(self, query_maxlen, model_type):
        #self.tok = BertTokenizerFast.from_pretrained('bert-base-uncased')
        self.tok = BertTokenizerFast.from_pretrained(model_type)
        self.query_maxlen = query_maxlen

        self.Q_marker_token, self.Q_marker_token_id = '[Q]', self.tok.convert_tokens_to_ids('[unused0]')
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

#
# In [3]: from colbert.modeling.tokenization import QueryTokenizer
# In [4]: t=QueryTokenizer(50)
# In [3]:  t.tensorize(['what is the answer?', 'is that not completely ridiculously false?'])
# Out[3]:
# (tensor([[ 101,    1, 2054, 2003, 1996, 3437, 1029,  102,  103,  103,  103,  103,
#            103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,
#            103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,
#            103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,
#            103,  103],
#          [ 101,    1, 2003, 2008, 2025, 3294, 9951, 2135, 6270, 1029,  102,  103,
#            103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,
#            103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,
#            103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,  103,
#            103,  103]]),
#  tensor([[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0],
#          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0]]))
# 
# In [7]: t.Q_marker_token_id
# Out[7]: 1
#
# In [9]: t.mask_token_id
# Out[9]: 103
#
# In [10]: t.cls_token_id
# Out[10]: 101

# In [11]: t.sep_token_id
# Out[11]: 102
#

