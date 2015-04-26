from __future__ import division
from collections import OrderedDict

import sys

# precision is the fraction of relevant (expected) documents that are successfully retrieved (actual).

# takes two dicts; one containing expected results and the other containing actual results
def calculate(expected_results, actual_results):
    # the query identifiers must match exactly
    assert( sorted(actual_results.keys()) == sorted(expected_results.keys()) )

    recalls = OrderedDict()

    for query_id,expected_document_ids in expected_results.iteritems():

        actual_document_ids    = actual_results[query_id]

        relevant_and_retrieved = filter(lambda el: el in expected_document_ids ,actual_document_ids) 

        recall                 = len(relevant_and_retrieved) / len(expected_document_ids)

        recalls[query_id]      = round(recall,3)

    # make sure all queries have been accounted for
    assert(sorted(actual_results.keys()) == sorted(expected_results.keys()) == sorted(recalls.keys()) )

    return(recalls)






