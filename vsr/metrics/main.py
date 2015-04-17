
from __future__ import division
from vsr.common.helpers import results as results_helper
from vsr.metrics.measures import f_score, mean_ap, precision, recall

import ConfigParser
import csv
import logging as log
import os,sys
import pprint as pp


current_file_location = os.path.dirname(os.path.realpath(__file__))

log_file    = '../../logs/vsr.log'
config_file = 'metrics.cfg'

FORMAT='%(asctime)s %(levelname)s: %(message)s'
DATEFMT='%d %b %H:%M:%S'
log.basicConfig(
	filename=current_file_location+'/'+log_file,
	level=log.DEBUG, 
	format=FORMAT,datefmt=DATEFMT,
	filemode='a') # append to previous log

log.info("Started module execution: 'metrics'")

config_file_absolute  = current_file_location+'/'+config_file
config                = ConfigParser.ConfigParser()
config.read(config_file_absolute)

# input files
expected_results_file = current_file_location+'/'+config.get('InputFiles','EXPECTED_RESULTS')
actual_results_file   = current_file_location+'/'+config.get('InputFiles','ACTUAL_RESULTS')

# output directory
output_directory      = current_file_location+'/'+config.get('OutputFiles','OUTPUT_DIRECTORY')+'/'

expected_results      = results_helper.load_from_csv_file(expected_results_file)
actual_results        = results_helper.load_from_csv_file(actual_results_file)

precisions            = precision.calculate(expected_results,actual_results)
recalls               = recall.calculate(expected_results,actual_results)
f1_scores             = f_score.calculate(expected_results,actual_results,beta=1)
mean_ap               = mean_ap.calculate(expected_results,actual_results)    

results_helper.write_to_csv_file(precisions,output_directory+'precisions.csv')
results_helper.write_to_csv_file(recalls,output_directory+'recalls.csv')
results_helper.write_to_csv_file(f1_scores,output_directory+'f1_scores.csv')

# mean_ap is a single number
with open(output_directory+'mean_ap.txt','w') as outfile:
	outfile.write(str(mean_ap))


log.info("Finished module execution: 'metrics'")