from pprint import pprint
from collections import OrderedDict
from vsr.common.helpers import dom,index,logger
from vsr.common.helpers.extras import merge_params
from xml.dom import minidom

import ConfigParser
import cPickle as pickle
import csv
import logging as log
import os
import sys

def run(override_params = None):

	current_file_location  = os.path.dirname(os.path.realpath(__file__))

	log                    = logger.init_log(current_file_location+'/../../logs/vsr.log')

	log.info("Started module execution: 'query_processor'")

	config_file            = 'pc.cfg'
	config_file_absolute   = current_file_location+'/'+config_file

	config                 = ConfigParser.ConfigParser()
	config.read(config_file_absolute)

	# input files (queries and results and the inverted index)
	input_file             = config.get('InputFiles','LEIA')
	inverted_index_file    = config.get('InputFiles','INVERTED_INDEX')

	# output files
	processed_queries_file = config.get('OutputFiles','CONSULTAS')
	expected_results_file  = config.get('OutputFiles','RESULTADOS')

	# params
	params                           = dict()
	params['TOKEN_LENGTH_THRESHOLD'] =  config.getint('Params','TOKEN_LENGTH_THRESHOLD')
	params['ONLY_LETTERS']           = config.getboolean('Params','ONLY_LETTERS')
	params['IGNORE_STOP_WORDS']      = config.getboolean('Params','IGNORE_STOP_WORDS')
	params['USE_STEMMER']            = config.getboolean('Params','USE_STEMMER')

	params                           = merge_params(params,override_params)

	# read query XML file containing queries
	absolute_input_file    = current_file_location+'/'+input_file
	xmldoc                 = minidom.parse(absolute_input_file)
	queries                = xmldoc.getElementsByTagName("QUERY")

	# work out the term vector representation for each query
	# it needs to be put through the EXACT_SAME processing
	# the documents went through (and include all tokens ever found in all documents)
	inverted_index_file_absolute = current_file_location+'/'+inverted_index_file

	inverted_index               = index.load_index_from_csv_file(inverted_index_file_absolute)
	global_tokens                = index.extract_tokens(inverted_index) 
	 
	# queries will first be placed here, in order to be processed
	# query_num => { 'tokens' => list_of_tokens, 'results'=> list_of_document_ids }
	queries_dict                 = OrderedDict()

	no_of_queries_read           = 0

	for query in queries:

		try:
			query_num     = dom.get_query_num(query)
			query_tokens  = dom.get_query_tokens(query,
							  token_space       = global_tokens,
							  min_token_length  = params['TOKEN_LENGTH_THRESHOLD'],
						      only_letters      = params['ONLY_LETTERS'],
						      ignore_stop_words = params['IGNORE_STOP_WORDS'],
						      use_stemmer       = params['USE_STEMMER'])

			hits_in_order = dom.get_results_sorted(query)
		except RuntimeError:
			log.warning("Found badly-formed query; skipped.")
			continue # couldn't find needed information, skip

		no_of_queries_read     += 1

		# yes, a dict with another dict inside
		inside_dict             = OrderedDict()
		inside_dict['tokens']   = query_tokens
		inside_dict['results']  = hits_in_order	
		queries_dict[query_num] = inside_dict
		

	log.info('Read {0} queries from file {1}'.format(no_of_queries_read,input_file))


	# for debugging purposes
	pickle_dump_file = current_file_location+'/'+'processed_queries_dict_pickle_dump.out'
	pickle.dump(queries_dict,open(pickle_dump_file,"wb"))

	# writing output
	expected_results_file_only_doc_ids = expected_results_file.replace('.csv','_only_doc_ids.csv')

	expected_results                   = open(current_file_location+'/'+expected_results_file,'w')
	processed_queries                  = open(current_file_location+'/'+processed_queries_file,'w')
	expected_results_only_doc_ids      = open(current_file_location+'/'+expected_results_file_only_doc_ids,'w')

	w_expected_results                 = csv.writer(expected_results,delimiter=";")
	w_processed_queries                = csv.writer(processed_queries,delimiter=";")
	w_expected_results_only_doc_ids    = csv.writer(expected_results_only_doc_ids,delimiter=";")

	for key,val in queries_dict.iteritems():
		w_expected_results_only_doc_ids.writerow([key,map(lambda x: x[0],val['results'])])
		w_expected_results.writerow([key,val['results']])
		w_processed_queries.writerow([key,val['tokens']])
		 
	# must close these explicitly because i'm not using the 'with open(...) as outfile' construct	 
	expected_results.close()
	processed_queries.close()
	expected_results_only_doc_ids.close()	 

	log.info("Finished module execution: 'query_processor'")
	print("Finished module execution: 'query_processor'")

if __name__ == "__main__":
	run()