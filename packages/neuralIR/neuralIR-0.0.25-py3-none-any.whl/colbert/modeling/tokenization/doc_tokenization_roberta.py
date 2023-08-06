import torch

from transformers import RobertaTokenizerFast
from colbert.modeling.tokenization.utils import _split_into_batches, _sort_by_length


class DocTokenizerRoberta():
    def __init__(self, doc_maxlen,model_type):
        self.tok = RobertaTokenizerFast.from_pretrained(model_type)
        self.doc_maxlen = doc_maxlen

        self.D_marker_token, self.D_marker_token_id = '[D]', self.tok.convert_tokens_to_ids('madeupword0001')

    # tokenizer is not used colbert code base, but is implemented in DocTokenizer
    def tokenize(self, batch_text, add_special_tokens=False):
        raise NotImplementedError()

    # encode is not used colbert code base, but is implemented in DocTokenizer
    def encode(self, batch_text, add_special_tokens=False):
        raise NotImplementedError()

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


# In [1]: from colbert.modeling.tokenization import DocTokenizerRoberta

# In [2]: t=DocTokenizerRoberta(50)

# In [3]: t.tensorize(['Here is the answer.', 'Another longer answer is here.'])
# Out[3]:
# (tensor([[    0, 50262,  1398,    16,     5,  1948,     4,     2,     1],
#          [    0, 50262,  2044,  1181,  1948,    16,   259,     4,     2]]),
#  tensor([[1, 1, 1, 1, 1, 1, 1, 1, 0],
#          [1, 1, 1, 1, 1, 1, 1, 1, 1]]))

# In [4]:  t.D_marker_token_id
# Out[4]: 50262

# In [5]: t.tok.decode(range(5))
# Out[5]: '<s><pad></s><unk>.'
