# bert imports
from colbert.modeling.colbert import ColBERT
from colbert.modeling.tokenization import QueryTokenizer, DocTokenizer

# roberta imports
from colbert.modeling.colbert_roberta import ColBERT_Roberta
from colbert.modeling.tokenization import QueryTokenizerRoberta, DocTokenizerRoberta

# xlmr imports
from colbert.modeling.colbert_xlmr import ColBERT_XLMR
from colbert.modeling.tokenization import QueryTokenizerXLMR, DocTokenizerXLMR

# mbert imports
from colbert.modeling.colbert_mbert import ColBERT_mbert
from colbert.modeling.tokenization import QueryTokenizerMBERT, DocTokenizerMBERT

import os

#----------------------------------------------------------------
def get_colbert_from_pretrained(model_type: str,
                                **kwargs):
    local_models_repository = kwargs.pop('local_models_repository', None)
    # model_name is hardcoded to "bert-base-uncased" thoughout ColBERT
    local_models_repository = kwargs.pop('local_models_repository', None)

    if not (model_type=='xlm-roberta-base' or model_type=='xlm-roberta-large'):
        kwargs.pop('distill_query_passage_separately')
        kwargs.pop('query_only')

    if model_type=='bert-base-uncased' or model_type=='bert-large-uncased':
        colbert = ColBERT.from_pretrained(model_type, **kwargs)
    elif model_type == 'tinybert':
        if not local_models_repository:
            raise ValueError("Please specify the local repository for additional models.")
        colbert = ColBERT.from_pretrained(os.path.join(local_models_repository, 'tinybert/TinyBERT_General_4L_312D'), **kwargs)
        # e.g. from https://huggingface.co/huawei-noah/TinyBERT_General_4L_312D/tree/main
    elif model_type=='roberta-base' or model_type=='roberta-large':
        colbert = ColBERT_Roberta.from_pretrained(model_type, **kwargs)
    elif model_type=='xlm-roberta-base' or model_type=='xlm-roberta-large':
        colbert = ColBERT_XLMR.from_pretrained(model_type, **kwargs)
    elif model_type=='bert-base-multilingual-cased' or model_type=='bert-base-multilingual-uncased':
        colbert = ColBERT_mbert.from_pretrained(model_type, **kwargs)
    else:
        raise NotImplementedError()

    colbert.model_type=model_type
    return colbert

#----------------------------------------------------------------
def get_query_tokenizer(model_type, maxlen):
    if model_type=='bert-base-uncased' or model_type=='bert-large-uncased':
        return QueryTokenizer(maxlen,model_type)
    elif model_type=='tinybert':
        return QueryTokenizer(maxlen, 'bert-base-uncased')
    elif model_type=='roberta-base' or model_type=='roberta-large':
        return QueryTokenizerRoberta(maxlen, model_type)
    elif model_type=='xlm-roberta-base' or model_type=='xlm-roberta-large':
        return QueryTokenizerXLMR(maxlen, model_type)
    elif model_type=='bert-base-multilingual-cased':
        return QueryTokenizerMBERT(maxlen, model_type)
    elif model_type=='bert-base-multilingual-uncased':
        return QueryTokenizerMBERT(maxlen, model_type)
    else:
        raise NotImplementedError()

#----------------------------------------------------------------
def get_doc_tokenizer(model_type, maxlen):
    if model_type=='bert-base-uncased' or model_type=='bert-large-uncased':
        return DocTokenizer(maxlen, model_type)
    elif model_type=='tinybert':
        return DocTokenizer(maxlen, 'bert-base-uncased')
    elif model_type=='roberta-base' or model_type=='roberta-large':
        return DocTokenizerRoberta(maxlen, model_type)
    elif model_type=='xlm-roberta-base' or model_type=='xlm-roberta-large':
        return DocTokenizerXLMR(maxlen, model_type)
    elif model_type=='bert-base-multilingual-cased':
        return DocTokenizerMBERT(maxlen, model_type)
    elif model_type=='bert-base-multilingual-uncased':
        return DocTokenizerMBERT(maxlen, model_type)
    else:
        raise NotImplementedError()
