from __future__ import division
from vsm.common.helpers.index import build_document_term_matrix,build_term_vector
from vsm.common.helpers.validators import ( 
	validate_weight_function,
	validate_positive_integer
)
import ConfigParser
import csv
import logging as log
import os,sys
import pprint as pp
import nltk

current_file_location = os.path.dirname(os.path.realpath(__file__))

log_file = '../../logs/vsm.log'
config_file = 'index.cfg'
config_section = 'Steps'

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

input_file          = config.get('Steps','LEIA')
output_file         = config.get('Steps','ESCREVA')
weighting_function  = config.get('Params','WEIGHT_FUNCTION')
validate_weight_function(weighting_function)

max_token_length    = config.getint('Params','TOKEN_LENGTH_THRESHOLD')
validate_positive_integer(max_token_length)

restrict_to_letters = config.getboolean('Params','ONLY_LETTERS')

# token => list of occurrences
inverted_index = dict()

input_file_absolute = current_file_location+'/'+input_file
with open(input_file_absolute,'rb') as csvfile:
	reader = csv.reader(csvfile,delimiter=';')

	for row in reader:
		token = row[0].strip()
		document_occurrences = map(lambda str: int(str),
			row[1].lstrip('[').rstrip(']').strip().split(','))

		inverted_index[token] = document_occurrences

# document => list of token weights
document_term_matrix = build_document_term_matrix(
	inverted_index, 
	weighting_function = weighting_function,
	max_token_length = max_token_length,
	only_letters = restrict_to_letters )

output_file_absolute = current_file_location+'/'+output_file

w = csv.writer(open(output_file_absolute,"w"),delimiter=";")

for key,val in document_term_matrix.iteritems():
	w.writerow([key,val])

log.info("Finished module execution: 'indexer'")