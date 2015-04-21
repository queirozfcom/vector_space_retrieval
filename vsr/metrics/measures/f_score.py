from __future__ import division
from collections import OrderedDict
from vsr.metrics.measures import precision,recall

import sys

# the f score produces a value that weights both recall and precision. The value beta (positive real) is 
#   the magnitude with which recall should be considered more important than precision. When beta is 1,
#   it means that both recall and precision are given equal weights
def calculate(expected_results,actual_results,beta=1):
	assert(expected_results.keys() == actual_results.keys())

	precisions   = precision.calculate(expected_results,actual_results)
	recalls      = recall.calculate(expected_results,actual_results)

	f_scores     = OrderedDict()

	for query_id,doc_id in expected_results.iteritems():
		p                  = precisions[query_id]
		r                  = recalls[query_id]

		try:
			f_score            = ( (1 + pow(beta,2) ) *( p * r ) ) / ( ( pow(beta,2) * p ) + r )
		except ZeroDivisionError:
			continue
			sys.exit()
			
		f_scores[query_id] = round(f_score,3)

	return(f_scores)