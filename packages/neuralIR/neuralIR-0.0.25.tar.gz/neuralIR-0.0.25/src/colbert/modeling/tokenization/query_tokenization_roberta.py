import torch

from transformers import RobertaTokenizerFast
from colbert.modeling.tokenization.utils import _split_into_batches

# special tokens available 
#    n      v
# 0  0    <s>
# 1  1  <pad>
# 2  2   </s>
# 3  3  <unk>
# 50260  50260   <|endoftext|>
# 50261  50261  madeupword0000
# 50262  50262  madeupword0001
# 50263  50263  madeupword0002
# 50264  50264          <mask>

class QueryTokenizerRoberta():
    def __init__(self, query_maxlen, model_type):
        self.tok = RobertaTokenizerFast.from_pretrained(model_type)
        self.query_maxlen = query_maxlen

        self.Q_marker_token, self.Q_marker_token_id = '[Q]', self.tok.convert_tokens_to_ids('madeupword0000')
#        self.cls_token, self.cls_token_id = self.tok.cls_token, self.tok.cls_token_id
#        self.sep_token, self.sep_token_id = self.tok.sep_token, self.tok.sep_token_id
        self.mask_token, self.mask_token_id = self.tok.pad_token, self.tok.pad_token_id

#        assert self.Q_marker_token_id == 1 and self.mask_token_id == 103

    # tokenizer is not used colbert code base, but is implemented in QueryTokenizer
    def tokenize(self, batch_text, add_special_tokens=False):
        raise NotImplementedError()

    # encode is not used colbert code base, but is implemented in QueryTokenizer
    def encode(self, batch_text, add_special_tokens=False):
        raise NotImplementedError()

    def tensorize(self, batch_text, bsize=None):
        assert type(batch_text) in [list, tuple], (type(batch_text))

        # add placehold for the [Q] marker
        batch_text = ['. ' + x for x in batch_text]

        obj = self.tok(batch_text, padding='max_length', truncation=True,
                       return_tensors='pt', max_length=self.query_maxlen)

        ids, mask = obj['input_ids'], obj['attention_mask']

        # postprocess for the [Q] marker and the [MASK] augmentation
        ids[:, 1] = self.Q_marker_token_id
#
# roberta tokenizer has pad_token_id=1, <s>=0, so the following statement must be omitted
#        ids[ids == 0] = self.mask_token_id
# I'm keeping commented-out code here in case of comparison with QueryTokenizer.py (bert)

        if bsize:
            batches = _split_into_batches(ids, mask, bsize)
            return batches

        return ids, mask



# In [1]: from colbert.modeling.tokenization import QueryTokenizerRoberta

# In [2]: t=QueryTokenizerRoberta(50)

# In [3]: t.tensorize(['what is the answer?', 'is that not completely ridiculously false?'])
# Out[3]:
# (tensor([[    0, 50261,    99,    16,     5,  1948,   116,     2,     1,     1,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1],
#          [    0, 50261,    16,    14,    45,  2198, 33785,  3950,   116,     2,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
#               1,     1,     1,     1,     1,     1,     1,     1,     1,     1]]),
#  tensor([[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0],
#          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           0, 0]]))

# In [4]: t.Q_marker_token_id
# Out[4]: 50261

# In [5]: t.mask_token_id
# Out[5]: 1

# In [6]: t.tok.decode(range(5))
# Out[6]: '<s><pad></s><unk>.'
