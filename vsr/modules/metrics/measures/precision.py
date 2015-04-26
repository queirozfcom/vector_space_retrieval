#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from collections import OrderedDict
# from sklearn.metrics import precision_recall_curve

import pylab as pl
import sys

# precision is the fraction of retrieved (actual) documents that are relevant (expected).

# takes two dicts; one containing expected results and the other containing actual results
# returns a dict { q_id => precision[q_id]}
def calculate(expected_results, actual_results, threshold = None):
    # the query identifiers must match exactly
    assert( sorted(actual_results.keys()) == sorted(expected_results.keys()) )

    precisions = OrderedDict()

    for query_id,expected_document_ids in expected_results.iteritems():
        actual_document_ids    = actual_results[query_id]

        if threshold is not None:
            # then i'll interpret is as a threshold for retrieved documents
            # in order words, P@n
            actual_document_ids = actual_document_ids[:threshold]

        relevant_and_retrieved = filter(lambda el: el in expected_document_ids ,actual_document_ids) 

        precision              = len(relevant_and_retrieved) / len(actual_document_ids)

        precisions[query_id]   = round(precision,3)

    # make sure all queries have been accounted for
    assert(sorted(actual_results.keys()) == sorted(expected_results.keys()) == sorted(precisions.keys()) )

    return(precisions)


# return pairs (recall,precision), one for each recall point provided
def calculate_points(sorted_expected_results,sorted_actual_results):
          
    recall_points = [0.0,0.1,0.2,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

    # list of pairs
    pairs = list()

    for recall_point in recall_points:
        # qual é a precisão do algoritmo se só considerarmos
        #   a proporção dada dos documentos relevantes retornados?

        new_pair                   = [recall_point]

        precisions_at_recall_point = list()

        for query_id,expected_document_ids in sorted_expected_results.iteritems():
            expected_results_for_query = expected_document_ids
            actual_results_for_query   = sorted_actual_results[query_id]

            precision                  = _precision_at_recall_point(
                                            expected_results_for_query,
                                            actual_results_for_query,
                                            recall_point)

            precisions_at_recall_point.append(precision)


        # the y-value is the average precision at point recall_point
        # over all queries
        average_precisions = sum(precisions_at_recall_point)/len(precisions_at_recall_point)
            
        new_pair.append(average_precisions)
        pairs.append(new_pair)
            
    return(pairs)    


# data uma lista de ids esperados e uma lista de ids recuperados, retorna a precisão
#   se só considerarmos o recall_point dado. Se o recall_point for 1.0, então o resultado
#   é a precisão normal
def _precision_at_recall_point(sorted_expected_doc_ids,sorted_actual_doc_ids,recall_point):
    assert( isinstance(recall_point,float) )

    # recall_point is given as a normalized proportion (from 0.0 to 1.0)
    recall_threshold = int(len(sorted_expected_doc_ids)*recall_point)

    # this is a little hack so as not to get division by zeros
    # this is the minimum recall, so maximum precision
    if recall_threshold == 0:
        recall_threshold = 1

    # these are the expected documents when only looking up to 
    # given recall threshold
    

    # ?
    # sorted_expected_doc_ids = sorted_expected_doc_ids[:recall_threshold]




    # similarly, we only consider relevant the retrieved documents in that same threshold
    # document_threshold      = int(len(sorted_actual_doc_ids)*recall_point)
    # sorted_actual_doc_ids   = sorted_actual_doc_ids 

    # relevant_and_retrieved  = _get_precision_at_absolute_recall(sorted_actual_doc_ids,sorted_actual_doc_ids,recall_threshold)
    # filter(lambda el: el in sorted_expected_doc_ids ,sorted_actual_doc_ids) 

    # if len(sorted_actual_doc_ids) == 0:
    #     # this means we're the first recall point
    #     assert(document_threshold == recall_threshold == 0)
    #     # this is needed for the algorithm to work
    #     # see http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html
    #     precision = 1.0
    # else:
    # precision = len(relevant_and_retrieved) / len(sorted_actual_doc_ids)

    # what precision do I get if we only consider the first <recall_threshold>
    #   expected results?
    precision = _get_precision_at_absolute_recall(
        sorted_expected_doc_ids,
        sorted_actual_doc_ids,
        recall_threshold)

    return(precision)

def _get_precision_at_absolute_recall(expected_results,actual_results,absolute_threshold):

    hits  = 0
    total = 0 

    for idx,actual_id in enumerate(actual_results):
        if hits >= absolute_threshold:
            return(hits/total)
        # if idx > absolute_threshold:
        #     # this will cause a threshold of 0 to return 1.0, which makes sense
        #     #  because minimum recall equals maximum precision, which is 1.0
        #     return(running_precision)
        if actual_id in expected_results:
            hits  += 1
            total += 1
        else:
            total += 1    

    return(hits/total)        