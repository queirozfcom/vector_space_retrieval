
from __future__ import division
from vsr.common.helpers import logger
from vsr.common.helpers import results as results_helper
from vsr.common.helpers import plot as plot_helper
from vsr.common.helpers.extras import merge_params
from vsr.modules.metrics.measures import f_score, mean_ap, precision, recall
# from vsr.metrics.measures import discounted_cumulative_gain as dcg

import ConfigParser
import csv
import logging as log
import os,sys
import pprint as pp

def run(override_params = None):

	current_file_location = os.path.dirname(os.path.realpath(__file__))

	log = logger.init_log(current_file_location+'/../../../logs/vsr.log')

	log.info("Started module execution: 'metrics'")

	config_file = 'metrics.cfg'

	config_file_absolute  = current_file_location+'/'+config_file
	config                = ConfigParser.ConfigParser()
	config.read(config_file_absolute)

	# input files
	expected_results_file      = current_file_location+'/'+config.get('InputFiles','EXPECTED_RESULTS')
	actual_results_file        = current_file_location+'/'+config.get('InputFiles','ACTUAL_RESULTS')
	expected_results_full_file = current_file_location+'/'+config.get('InputFiles','EXPECTED_RESULTS_FULL')
	actual_results_full_file   = current_file_location+'/'+config.get('InputFiles','ACTUAL_RESULTS_FULL')

	# output directory
	output_directory      = current_file_location+'/'+config.get('OutputFiles','OUTPUT_DIRECTORY')+'/'

	#params
	params                = dict()
	params                = merge_params(params,override_params)

	# loading the files to memory
	expected_results      = results_helper.load_from_csv_file(expected_results_file)
	actual_results        = results_helper.load_from_csv_file(actual_results_file)

	# calculating the actual metrics
	precisions            = precision.calculate(expected_results,actual_results)
	recalls               = recall.calculate(expected_results,actual_results)
	f1_scores             = f_score.calculate(expected_results,actual_results,beta=1)
	mean_ap_value         = mean_ap.calculate(expected_results,actual_results)    
	precisions_at_10      = precision.calculate(expected_results,actual_results,threshold=10)
	precision_11_points   = precision.calculate_points(expected_results,actual_results)

	# TODO DCG
	# discounted_cumulative_gain = dcg.calculate(expected_results,actual_results, rank_threshold = 10)

	# write output to csv files
	results_helper.write_to_csv_file(precisions,output_directory+'precisions.csv')
	results_helper.write_to_csv_file(recalls,output_directory+'recalls.csv')
	results_helper.write_to_csv_file(f1_scores,output_directory+'f1_scores.csv')
	results_helper.write_to_csv_file(precisions_at_10,output_directory+'precisions_at_10.csv')
	results_helper.write_to_csv_file(precision_11_points,output_directory+'precision_11_points.csv')

	# TODO DCG
	#results_helper.write_to_csv_file(discounted_cumulative_gain,output_directory+'dcg.csv')

	# mean_ap is a single number
	with open(output_directory+'mean_ap.txt','w') as outfile:
	    outfile.write(str(mean_ap_value))

	
	if "USE_STEMMER" in params.keys():
		title = "Precision-Recall curve USING STEMMER = '{0}'".format(params['USE_STEMMER'])
	else:
		title = "Precision-Recall curve"

	# and 11 points is better shown in graph form	
	plot_helper.plot_recall_precision_curve(
		precision_11_points,
		title = title,
		display = False,
		filename = output_directory+'precision_11_points.png' )

	log.info("Finished module execution: 'metrics'")
	print("Finished module execution: 'metrics'")

if __name__ == "__main__":
	run()	