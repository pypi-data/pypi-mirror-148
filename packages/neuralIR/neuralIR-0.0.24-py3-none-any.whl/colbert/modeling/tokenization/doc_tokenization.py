import torch

from transformers import BertTokenizerFast
from colbert.modeling.tokenization.utils import _split_into_batches, _sort_by_length


class DocTokenizer():
    def __init__(self, doc_maxlen, model_type):
        #self.tok = BertTokenizerFast.from_pretrained('bert-base-uncased')
        self.tok = BertTokenizerFast.from_pretrained(model_type)
        self.doc_maxlen = doc_maxlen

        self.D_marker_token, self.D_marker_token_id = '[D]', self.tok.convert_tokens_to_ids('[unused1]')
        self.cls_token, self.cls_token_id = self.tok.cls_token, self.tok.cls_token_id
        self.sep_token, self.sep_token_id = self.tok.sep_token, self.tok.sep_token_id

        assert self.D_marker_token_id == 2

    def tokenize(self, batch_text, add_special_tokens=False):
        assert type(batch_text) in [list, tuple], (type(batch_text))

        tokens = [self.tok.tokenize(x, add_special_tokens=False) for x in batch_text]

        if not add_special_tokens:
            return tokens

        prefix, suffix = [self.cls_token, self.D_marker_token], [self.sep_token]
        tokens = [prefix + lst + suffix for lst in tokens]

        return tokens

    def encode(self, batch_text, add_special_tokens=False):
        assert type(batch_text) in [list, tuple], (type(batch_text))

        ids = self.tok(batch_text, add_special_tokens=False)['input_ids']

        if not add_special_tokens:
            return ids

        prefix, suffix = [self.cls_token_id, self.D_marker_token_id], [self.sep_token_id]
        ids = [prefix + lst + suffix for lst in ids]

        return ids

    def tensorize(self, batch_text, bsize=None):
        assert type(batch_text) in [list, tuple], (type(batch_text))

        # add placehold for the [D] marker
        batch_text = ['. ' + x for x in batch_text]

        obj = self.tok(batch_text, padding='longest', truncation='longest_first',
                       return_tensors='pt', max_length=self.doc_maxlen)

        ids, mask = obj['input_ids'], obj['attention_mask']

        # postprocess for the [D] marker
        ids[:, 1] = self.D_marker_token_id

        if bsize:
            ids, mask, reverse_indices = _sort_by_length(ids, mask, bsize)
            batches = _split_into_batches(ids, mask, bsize)
            return batches, reverse_indices

        return ids, mask


# In [1]: from colbert.modeling.tokenization import DocTokenizer

# In [2]: t=DocTokenizer(50)

# In [3]: t.tensorize(['Here is the answer.', 'Another longer answer is here.'])
# Out[3]:
# (tensor([[ 101,    2, 2182, 2003, 1996, 3437, 1012,  102,    0],
#          [ 101,    2, 2178, 2936, 3437, 2003, 2182, 1012,  102]]),
#  tensor([[1, 1, 1, 1, 1, 1, 1, 1, 0],
#          [1, 1, 1, 1, 1, 1, 1, 1, 1]]))

# In [4]: t.D_marker_token_id
# Out[4]: 2

# In [6]: t.cls_token_id
# Out[6]: 101

# In [7]: t.sep_token_id
# Out[7]: 102
