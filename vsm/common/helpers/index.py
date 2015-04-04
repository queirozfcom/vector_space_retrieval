from __future__ import division
from nltk.tokenize import word_tokenize

import math
import pprint as pp
import nltk
import sys

# dict should be a dictionary with identifiers as keys and a list of tokens
# as value
def build_inverted_index(tokens,count_duplicates=False):
    index = dict()
    for key,token_list in tokens.iteritems():
        
        token_list_upper = map(lambda x: x.upper(), token_list)

        for token_upper in set(token_list_upper):

            # I'm not supposed to optimize it here
            # if not token_upper.isalpha():
            #   continue

            if token_upper not in index:
                index[token_upper] = list()

            if(count_duplicates):   
                for i in range(token_list_upper.count(token_upper)):
                    index[token_upper].append(key) # as many times as it appears                
            else:
                index[token_upper].append(key) # just once

    return(index)           

def get_tokens(text):
    return(word_tokenize(text))


def build_document_term_matrix(inverted_index, weighting_function, max_token_length, only_letters):
    
    term_list = build_term_vector(inverted_index, weighting_function, max_token_length, only_letters)

    document_id_list = _get_identifier_list(inverted_index)

    total_number_of_documents = len(document_id_list)

    inverse_doc_frequencies = _get_inverse_document_frequencies(total_number_of_documents, inverted_index)    

    # with open('term_list.out','w') as out:
    #     pp.pprint(term_list, stream=out, indent=1)

    # sys.exit()

    # finished gathering the pieces, now for the actual matrix
    matrix = dict()

    for document_id in document_id_list:

        term_weights = list()

        for term in term_list:
            idf = inverse_doc_frequencies[term]
            tf  = _get_raw_term_frequency(term,document_id,inverted_index)

            tf_idf = round(tf * idf,3)

            term_weights.append(tf_idf)

        matrix[document_id] = term_weights

    return(matrix)

# Extract a list of all terms (keys in the inverted index). Terms will be normalized and possibly
#   ignored altogether depending on parameters passed
def build_term_vector(inverted_index, weighting_function, max_token_length, only_letters):
    
    term_vector = list()

    for raw_token in inverted_index.keys():
        term = raw_token.upper().strip()

        if len(term) < max_token_length:
            continue

        if only_letters:
            if not term.isalpha():
                continue

        term_vector.append(term)

    return(term_vector)

# Return all document identifiers that appear at least once in the inverted index
def _get_identifier_list(inverted_index):
    identifiers = list()

    for document_list in inverted_index.values():
        for identifier in document_list:
            if identifier not in identifiers:
                identifiers.append(identifier)

    return(identifiers)

# Return a dict where keys are terms and values are the inverse document
#   frequency (IDF) for that term in the documents in inverted_index
def _get_inverse_document_frequencies(n,inverted_index):
    inverse_document_frequencies = dict()

    for term,hits in inverted_index.iteritems():
        doc_count = len(set(hits))
        inverse_document_frequencies[term] = math.log(n/doc_count)

    return(inverse_document_frequencies)

# Return the number of times a given term appears in a given document
def _get_raw_term_frequency(term,document_identifier,inverted_index):
    frequency = len([ id for id in inverted_index[term] if id == document_identifier] )
    return(frequency)
