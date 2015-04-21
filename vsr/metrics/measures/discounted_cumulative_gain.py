
from collections import OrderedDict

# returns a 
def calculate(expected_results,actual_results,rank_threshold=10):
	
	if not normalize:
		raise RuntimeError("Only normalized DCG is available right now. Are you really sure you know what you are doing?")

	expected_results_normalized = _normalize_and_replace_relevance_by_dcg(expected_results)
	actual_results_normalized   = _normalize_and_replace_distance_with_similarity(actual_results)


	

# sample line in expected results:
#  1;[[533, '2222'], [139, '1222'], [441, '2122'], [151, '2211']]
def _normalize_and_replace_relevance_by_dcg(expected_results):
	
	dict = OrderedDict()

	# the highest value for a rankstring is 8, i.e.
	#  2+2+2+2. And the lowest is zero.

	for q_id, results in expected_results.iteritems():
		for idx,(doc_id,rankstring) in enumerate(results):
			value = _sum_votes(rankstring)



# sample line in actual results:
#  1;[[1, 437, 0.719], [2, 498, 0.77], [3, 484, 0.789], [4, 957, 0.814]
# query_id;[[rank, doc_id, distance].....


def _sum_votes(numeric_string):
    sum = 0

    for idx in range(len(str(numeric_string))):
        sum += int(numeric_string[idx])

    return(sum) 