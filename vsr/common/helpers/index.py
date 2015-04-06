from __future__ import division
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from vsr.common.helpers.validators import validate_positive_integer

import csv
import math
import pprint as pp
import nltk
import sys

# Returns an inverted index (a dict where keys are terms and values are document identifiers)
#   from a token list. The token list should be a dict where keys are document identifiers and 
#   values are the list of tokens present in that document
def build_inverted_index(tokens,count_duplicates=False, min_token_length=2, only_letters = True, remove_stop_words = True):
    index = dict()
    for key,token_list in tokens.iteritems():
        
        token_list_upper = map(lambda x: x.upper(), token_list)

        for token_upper in set(token_list_upper):

            # optimizations start
            if only_letters:
                if not token_upper.isalpha():
                    continue

            if len(token_upper) < min_token_length:
                continue

            if remove_stop_words:
                stop = stopwords.words('english')
                # a few extra stopwords for us
                stop += set(('medical','however','diagnosis','fibrosis','used','cystic','observed','patient','patients','per','disease','diseases','cf')) 
                if token_upper.lower() in stop:
                    continue

            # optimizations end


            if token_upper not in index:
                index[token_upper] = list()

            if(count_duplicates):   
                for i in range(token_list_upper.count(token_upper)):
                    index[token_upper].append(key) # as many times as it appears                
            else:
                index[token_upper].append(key) # just once

    return(index)           
    
# Return all tokens present in a text.
def get_tokens(text):
    return(word_tokenize(text))

# Build a dict where the keys are document identifiers and values are term vectors.
def build_document_term_matrix(inverted_index, weighting_function, min_token_length, only_letters):
    
    if weighting_function not in ['tf-idf']:
        raise ValueError("Invalid weighting function. Available values are {0}".format(supported_weighting_functions))

    validate_positive_integer(min_token_length)    

    term_list = build_term_vector(inverted_index, weighting_function, min_token_length, only_letters)

    document_id_list = _get_identifier_list(inverted_index)

    total_number_of_documents = len(document_id_list)

    inverse_doc_frequencies = _get_inverse_document_frequencies(total_number_of_documents, inverted_index)    

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
def build_term_vector(inverted_index, weighting_function, min_token_length, only_letters):
    
    term_vector = list()

    for raw_token in inverted_index.keys():
        term = raw_token.upper().strip()

        if len(term) < min_token_length:
            continue

        if only_letters:
            if not term.isalpha():
                continue

        term_vector.append(term)

    return(term_vector)

def load_index_from_csv_file(absolute_path_to_file):
    inverted_index = dict()

    with open(absolute_path_to_file,'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')

        for row in reader:
            token = row[0].strip()
            document_occurrences = map(lambda str: int(str),
                row[1].lstrip('[').rstrip(']').strip().split(','))

            inverted_index[token] = document_occurrences

    return(inverted_index)

def extract_tokens(inverted_index):
    return(inverted_index.keys())


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
