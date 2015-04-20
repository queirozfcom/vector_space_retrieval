from collections import OrderedDict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vsr.vendor.PorterStemmer import PorterStemmer
from xml.dom import minidom

import sys

def get_num(record_node):
    maybe_recordnums = record_node.getElementsByTagName("RECORDNUM")

    if(len(maybe_recordnums)==0):
        raise RuntimeError("Node must have 'RECORDNUM' subnode!")
    elif(len(maybe_recordnums) != 1):
        raise RuntimeError("Node must have only one 'RECORDNUM' subnode!")
    else:
        return(int(maybe_recordnums[0].firstChild.nodeValue))   

def get_contents(record_node):
    node_num = get_num(record_node)
    maybe_abstracts = record_node.getElementsByTagName("ABSTRACT")
    maybe_extracts  = record_node.getElementsByTagName("EXTRACT")

    if(len(maybe_extracts) == 0 and len(maybe_abstracts) ==0):  
        raise RuntimeError("Node ",node_num," has neither 'EXTRACT' nor 'ABSTRACT' subnodes!")  
    elif(len(maybe_extracts) != 0 and len(maybe_abstracts) != 0):
        raise RuntimeError("Node ",node_num," must have only one of the following subnodes: 'EXTRACT','ABSTRACT'!")
    elif(len(maybe_extracts) == 0 and len(maybe_abstracts) != 0 ):
        return(maybe_abstracts[0].firstChild.nodeValue)
    elif(len(maybe_extracts) != 0 and len(maybe_abstracts) == 0):
        return(maybe_extracts[0].firstChild.nodeValue.strip())  


def get_query_num(query_node):
    maybe_nums = query_node.getElementsByTagName("QueryNumber")

    if(len(maybe_nums)==0):
        raise RuntimeError("Node must have 'QueryNumber' subnode!")
    elif(len(maybe_nums) != 1):
        raise RuntimeError("Node must have only one 'QueryNum' subnode!")
    else:
        return(int(maybe_nums[0].firstChild.nodeValue))

    
def get_query_tokens(query_node, token_space, min_token_length = 2, only_letters = False, ignore_stop_words = True, use_stemmer = False):
    
    stemmer            = PorterStemmer() 

    query_text_upper   = _get_query_text(query_node).upper()

    valid_query_tokens = list()

    token_candidates   = word_tokenize(query_text_upper)

    for possible_token_upper in token_candidates:

        if len(possible_token_upper.strip()) < min_token_length:
            continue

        if ignore_stop_words:
            stop  = stopwords.words('english')
            # a few extra stopwords for us
            stop += set(('medical','however','diagnosis','fibrosis','used','cystic','observed','patient','patients','per','disease','diseases','cf')) 
            if possible_token_upper.lower() in stop:
                continue    

        if only_letters:
            if not possible_token_upper.strip().isalpha():
                continue

        if use_stemmer:
            possible_token_upper = stemmer.stem(possible_token_upper.lower(),0,len(possible_token_upper)-1).upper()       

        valid_query_tokens.append(possible_token_upper.strip())


    term_vector = list()

    for token in token_space:
        if token in valid_query_tokens:
            term_vector.append(float(1))
        else:
            term_vector.append(float(0))

    return(term_vector)


def get_results_sorted(query_node):
    
    maybe_doc_nodes = query_node.getElementsByTagName("Item")

    if(len(maybe_doc_nodes)==0):
        raise RuntimeError("Node must have at least one 'Item' subnode")
    else:
        doc_scores = list()
        for doc_node in maybe_doc_nodes:
            score         = str(doc_node.attributes["score"].nodeValue)
            doc_id        = int(doc_node.firstChild.nodeValue)
            
            doc_scores.append([doc_id,score])


    doc_scores_ordered = sorted(doc_scores,key = lambda elem: _sum_votes(elem[1]), reverse= True)       

    # doc_scores_ordered = OrderedDict(sorted(doc_scores.items(),reverse=True, key = lambda elem:elem[1] ))

    return(doc_scores_ordered)      

def _sum_votes(numeric_string):
    sum = 0

    for idx in range(len(str(numeric_string))):
        sum += int(numeric_string[idx])

    return(sum)    

def _get_query_text(query_node):
    maybe_texts = query_node.getElementsByTagName("QueryText")

    if(len(maybe_texts)==0):
        raise RuntimeError("Node must have 'QueryText' subnode!")
    elif(len(maybe_texts) != 1):
        raise RuntimeError("Node must have only one 'QueryText' subnode!")
    else:
        text = maybe_texts[0].firstChild.nodeValue.strip()
        return(text)