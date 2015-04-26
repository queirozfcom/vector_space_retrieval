from __future__ import division
from vsr.common.helpers import index,logger
from vsr.common.helpers.extras import merge_params

import ConfigParser
import cPickle as pickle
import csv
import os,sys
import pprint as pp
import nltk

def run(override_params = None):

	current_file_location = os.path.dirname(os.path.realpath(__file__))

	log = logger.init_log(current_file_location+'/../../../logs/vsr.log')

	config_file = 'index.cfg'

	log.info("Started module execution: 'indexer'")

	config_file_absolute = current_file_location+'/'+config_file
	config               = ConfigParser.ConfigParser()
	config.read(config_file_absolute)

	# files
	input_file           = config.get('InputFiles','LEIA')
	output_file          = config.get('OutputFiles','ESCREVA')

	# params
	params                      = dict()
	params['WEIGHT_FUNCTION']   = config.get('Params','WEIGHT_FUNCTION')

	params                      = merge_params(params,override_params)

	# token => list of occurrences
	input_file_absolute  = current_file_location+'/'+input_file
	inverted_index       = index.load_index_from_csv_file(input_file_absolute)

	# document => list of token weights
	document_term_matrix = index.build_document_term_matrix(
		inverted_index, 
		weighting_function = params['WEIGHT_FUNCTION'])


	# for debugging purposes
	pickle_dump_file     = current_file_location+'/'+'document_term_dict_pickle_dump.out'
	pickle.dump(document_term_matrix,open(pickle_dump_file,"wb"))

	output_file_absolute = current_file_location+'/'+output_file

	with open(output_file_absolute,"w") as outfile:
		w = csv.writer(outfile, delimiter=";")

		for key,val in document_term_matrix.iteritems():
			w.writerow([key,val])

	log.info("Finished module execution: 'indexer'")
	print("Finished module execution: 'indexer'")

if __name__ == "__main__":
	run()