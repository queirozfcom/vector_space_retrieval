from __future__ import division
from vsr.common.helpers.index import (
	build_document_term_matrix,
	build_term_vector,
	load_index_from_csv_file)

import ConfigParser
import csv
import logging as log
import os,sys
import pprint as pp
import nltk

current_file_location = os.path.dirname(os.path.realpath(__file__))

log_file = '../../logs/vsr.log'
config_file = 'index.cfg'

FORMAT='%(asctime)s %(levelname)s: %(message)s'
DATEFMT='%d %b %H:%M:%S'
log.basicConfig(
	filename=current_file_location+'/'+log_file,
	level=log.DEBUG, 
	format=FORMAT,datefmt=DATEFMT,
	filemode='a') # append to previous log

log.info("Started module execution: 'indexer'")

config_file_absolute = current_file_location+'/'+config_file

config = ConfigParser.ConfigParser()
config.read(config_file_absolute)

# files
input_file          = config.get('Steps','LEIA')
output_file         = config.get('Steps','ESCREVA')

# options
weighting_function  = config.get('Params','WEIGHT_FUNCTION')
min_token_length    = config.getint('Params','TOKEN_LENGTH_THRESHOLD')
restrict_to_letters = config.getboolean('Params','ONLY_LETTERS')

# token => list of occurrences
input_file_absolute = current_file_location+'/'+input_file
inverted_index = load_index_from_csv_file(input_file_absolute)

# document => list of token weights
document_term_matrix = build_document_term_matrix(
	inverted_index, 
	weighting_function = weighting_function,
	min_token_length = min_token_length,
	only_letters = restrict_to_letters )

output_file_absolute = current_file_location+'/'+output_file

w = csv.writer(open(output_file_absolute,"w"),delimiter=";")

for key,val in document_term_matrix.iteritems():
	w.writerow([key,val])

log.info("Finished module execution: 'indexer'")