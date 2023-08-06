import string
import torch
import torch.nn as nn

from transformers import XLMRobertaModel, XLMRobertaTokenizer, BertPreTrainedModel
from colbert.parameters import DEVICE
from scipy import spatial
import numpy as np
import copy

class ColBERT_XLMR(BertPreTrainedModel):
    def __init__(self, config, query_maxlen, doc_maxlen, mask_punctuation, dim=128, similarity_metric='cosine', distill_query_passage_separately=False, query_only=False):

        super(ColBERT_XLMR, self).__init__(config)

        self.query_maxlen = query_maxlen
        self.doc_maxlen = doc_maxlen
        self.similarity_metric = similarity_metric
        self.dim = dim

        self.mask_punctuation = mask_punctuation
        self.skiplist = {}
        self.distill_query_passage_separately = distill_query_passage_separately
        self.query_only = query_only

        if self.mask_punctuation:
            self.tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')
            self.skiplist = {w: True
                             for symbol in string.punctuation
                             for w in [symbol, self.tokenizer.encode(symbol, add_special_tokens=False)[0]]}

        self.roberta = XLMRobertaModel(config)
        self.linear = nn.Linear(config.hidden_size, dim, bias=False)

        self.init_weights()

    def forward(self, Q, D):
        if self.distill_query_passage_separately :
            if self.query_only:
                return self.query(*Q)
            else :
                return self.score(self.query(*Q), self.doc(*D)), self.query(*Q), self.doc(*D)
        else:
            return self.score(self.query(*Q), self.doc(*D))

    def distance_calculation(self, ids, outputs):
        queries = self.tokenizer.batch_decode(ids)
        tokens = [self.tokenizer.tokenize(query) for query in queries]
        length = len(ids)
        en_tokens = tokens[0]
        en_outputs = outputs[0]
        other_tokens = tokens[0:length//2]
        other_outputs = outputs[0:length//2]
        with open("distance.txt", "w") as f:
            for lan_idx, other_output in enumerate(other_outputs):
                all_distance = []
                tokenList = '## ' + ' '.join([str(elem) for elem in other_tokens[lan_idx][:]])
                f.write(tokenList)
                f.write('\n')
                for en_token_idx, en_token_output in enumerate(en_outputs[:]):
                    distance = []
                    for ot_token_idx, other_token_output in enumerate(other_output):
                        dis = spatial.distance.cosine(en_token_output.cpu().detach(), other_token_output.cpu().detach())
                        distance.append(dis)
                    disList = ' '.join([str(elem) for elem in distance])
                    disList = str(en_tokens[en_token_idx]) + ' ' + disList
                    f.write(disList)
                    f.write('\n')
                    all_distance += distance
                all_distance_array = np.array(all_distance).reshape((self.query_maxlen,self.query_maxlen))
                alignment = self.align(all_distance_array)
                new_order_outputs = en_outputs.cpu().detach()
                new_order_en_tokens = copy.deepcopy(en_tokens)
                for swap in alignment:
                    new_order_outputs[[swap[0], swap[1]]] = new_order_outputs[[swap[1], swap[0]]]
                    new_order_en_tokens[swap[0]], new_order_en_tokens[swap[1]] = new_order_en_tokens[swap[1]], new_order_en_tokens[swap[0]]
                f.write("after alignment:\n")
                f.write(tokenList)
                f.write('\n')
                for en_token_idx, en_token_output in enumerate(new_order_outputs[:]):
                    distance = []
                    for ot_token_idx, other_token_output in enumerate(other_output):
                        dis = spatial.distance.cosine(en_token_output.cpu().detach(), other_token_output.cpu().detach())
                        distance.append(dis)
                    disList = ' '.join([str(elem) for elem in distance])
                    disList = str(new_order_en_tokens[en_token_idx]) + ' ' + disList
                    f.write(disList)
                    f.write('\n')
        return None
    
    def align(self, distance_array):
        swaps = []
        for i in range(self.query_maxlen):
            minValue = np.amin(distance_array)
            indexs = np.where(distance_array == np.amin(minValue))
            #get the index of the first min value
            i, j = indexs[0][0], indexs[1][0]
            #swap arrary row i and row j 
            distance_array[[i, j]] = distance_array[[j, i]]
            distance_array[j, :] = 10  #anything larger than 1 to avoid double count
            distance_array[:, j] = 10 
            swaps.append((i,j))
        return swaps

    def query(self, input_ids, attention_mask):
        # import pdb; pdb.set_trace()
        input_ids, attention_mask = input_ids.to(DEVICE), attention_mask.to(DEVICE)
        Q = self.roberta(input_ids, attention_mask=attention_mask)[0]
        # with open("student_eval.txt", "w") as f:
        #     for parm in self.roberta.parameters():
        #         f.write(str(parm))
        #     f.write("end of parms \n")
        #     f.write("input_ids:\n")
        #     f.write(str(input_ids))
        #     f.write('\n')
        #     f.write(str(attention_mask))
        #     f.write('\nQ:\n')
        #     f.write(str(Q))
        # self.distance_calculation(input_ids, Q)
        Q = self.linear(Q)
        # self.distance_calculation(input_ids, Q)

        return torch.nn.functional.normalize(Q, p=2, dim=2)

    def doc(self, input_ids, attention_mask, keep_dims=True):
        input_ids, attention_mask = input_ids.to(DEVICE), attention_mask.to(DEVICE)
        D = self.roberta(input_ids, attention_mask=attention_mask)[0]
        D = self.linear(D)

        mask = torch.tensor(self.mask(input_ids), device=DEVICE).unsqueeze(2).float()
        D = D * mask

        D = torch.nn.functional.normalize(D, p=2, dim=2)

        if not keep_dims:
            D, mask = D.cpu().to(dtype=torch.float16), mask.cpu().bool().squeeze(-1)
            D = [d[mask[idx]] for idx, d in enumerate(D)]

        return D

    def score(self, Q, D):
        if self.similarity_metric == 'cosine':
            return (Q @ D.permute(0, 2, 1)).max(2).values.sum(1)

        assert self.similarity_metric == 'l2'
        return (-1.0 * ((Q.unsqueeze(2) - D.unsqueeze(1)) ** 2).sum(-1)).max(-1).values.sum(-1)

    def mask(self, input_ids):
        mask = [[(x not in self.skiplist) and (x != 0) for x in d] for d in input_ids.cpu().tolist()]
        return mask
