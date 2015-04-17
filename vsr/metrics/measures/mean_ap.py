from __future__ import division
from vsr.metrics.measures.precision import calculate as calculate_precision

import sys

# mean average precision for a set of queries is the mean of the average precision scores for each query
def calculate(expected_results,actual_results):
	precisions         = calculate_precision(expected_results,actual_results)

	sum_of_precisions  = reduce(lambda acc,elem: acc + elem, precisions.values())
	mean_avg_precision = round(sum_of_precisions/len(precisions.values()),3)

	return(mean_avg_precision) 






