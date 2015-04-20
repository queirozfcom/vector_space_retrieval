from __future__ import division
from collections import OrderedDict

import sys

# precision is the fraction of retrieved (actual) documents that are relevant (expected).

# takes two dicts; one containing expected results and the other containing actual results
def calculate(expected_results, actual_results, at = None):
    # the query identifiers must match exactly
    assert( sorted(actual_results.keys()) == sorted(expected_results.keys()) )

    precisions = OrderedDict()

    for query_id,expected_document_ids in expected_results.iteritems():
        actual_document_ids    = actual_results[query_id]

        if at is not None:
            actual_document_ids = actual_document_ids[:at]

            # print(actual_document_ids)
            # sys.exit()

        relevant_and_retrieved = filter(lambda el: el in expected_document_ids ,actual_document_ids) 

        precision              = len(relevant_and_retrieved) / len(actual_document_ids)

        precisions[query_id]   = round(precision,3)

    # make sure all queries have been accounted for
    assert(sorted(actual_results.keys()) == sorted(expected_results.keys()) == sorted(precisions.keys()) )

    return(precisions)




