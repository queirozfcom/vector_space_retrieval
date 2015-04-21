from __future__ import division
from collections import OrderedDict
from vsr.common.classes import MultiOrderedDict
from vsr.common.helpers import dom,index,logger
from vsr.common.helpers.extras import str2bool,merge_params
from vsr.vendor.PorterStemmer import PorterStemmer

from xml.dom import minidom

import ConfigParser
import cPickle as pickle
import csv
import os
import nltk
import toolz.dicttoolz as dt
import sys

def run(override_params = None):

	current_file_location            = os.path.dirname(os.path.realpath(__file__))

	log                              = logger.init_log(current_file_location+'/../../logs/vsr.log',mode='w')
	log.info("Started module execution: 'inverted_index'")

	config_file                      = 'gli.cfg'
	config_file_absolute             = current_file_location+'/'+config_file

	config                           = ConfigParser.RawConfigParser(dict_type=MultiOrderedDict)
	config.read(config_file_absolute)

	# files
	input_files                      = config.get('InputFiles','LEIA')
	output_files                     = config.get('OutputFiles','ESCREVA')

	# params
	# it's an array because we're using MultiOrderedDict
	params                           = dict()
	params['TOKEN_LENGTH_THRESHOLD'] = int(config.get('Params','TOKEN_LENGTH_THRESHOLD')[0])
	params['ONLY_LETTERS']           = str2bool(config.get('Params','ONLY_LETTERS')[0])
	params['IGNORE_STOP_WORDS']      = str2bool(config.get('Params','IGNORE_STOP_WORDS')[0])
	params['USE_STEMMER']            = str2bool(config.get('Params','USE_STEMMER')[0])

	params                           = merge_params(params,override_params)

	articles                         = OrderedDict()

	for file in input_files:
		absolute_file       = current_file_location+'/'+file
		xmldoc              = minidom.parse(absolute_file)
		
		records             = xmldoc.getElementsByTagName("RECORD")

		no_of_articles_read = 0

		for record in records:

			record_num = dom.get_num(record)
			try:
				contents = dom.get_contents(record)
			except RuntimeError:
				log.warning("Found article with no contents ({0}); skipped.".format(record_num))
				continue # couldn't find article contents, skip

			no_of_articles_read += 1	
			articles[record_num] = contents
			
		log.info('Read {0} articles from file {1}'.format(no_of_articles_read,file))

	tokens           = dt.valmap(index.get_tokens,articles)

	inverted_index   = index.build_inverted_index(
			tokens            = tokens,
			remove_stop_words = params['IGNORE_STOP_WORDS'],
			count_duplicates  = True,
			min_token_length  = params['TOKEN_LENGTH_THRESHOLD'],
			only_letters      = params['ONLY_LETTERS'],
			use_stemmer       = params['USE_STEMMER'])

	# for debugging purposes only
	pickle_dump_file = current_file_location+'/'+'inverted_index_dict_pickle_dump.out'
	pickle.dump(inverted_index,open(pickle_dump_file,"wb"))

	for file in output_files:
		absolute_file = current_file_location+'/'+file
		
		with(open(absolute_file,"w")) as outfile:
			w = csv.writer(outfile,delimiter=';')

			for key,val in inverted_index.iteritems():
				w.writerow([key,val])

	log.info("Finished module execution: 'inverted_index'")
	print("Finished module execution: 'inverted_index'")

if __name__ == "__main__":
	run()