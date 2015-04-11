from __future__ import division
from collections import OrderedDict
from vsr.common.classes import MultiOrderedDict
from vsr.common.helpers import dom,index
from xml.dom import minidom

import ConfigParser
import cPickle as pickle
import csv
import logging as log
import os
import nltk
import toolz.dicttoolz as dt


current_file_location = os.path.dirname(os.path.realpath(__file__))

log_file          = '../../logs/vsr.log'
config_file       = 'gli.cfg'

FORMAT='%(asctime)s %(levelname)s: %(message)s'
DATEFMT='%d %b %H:%M:%S'
log.basicConfig(
	filename=current_file_location+'/'+log_file,
	level=log.DEBUG, 
	format=FORMAT,datefmt=DATEFMT,
	filemode='w') # start new log file

log.info("Started module execution: 'inverted_index'")

config_file_absolute = current_file_location+'/'+config_file

config               = ConfigParser.RawConfigParser(dict_type=MultiOrderedDict)
config.read(config_file_absolute)

# files
input_files          = config.get('InputFiles','LEIA')
output_files         = config.get('OutputFiles','ESCREVA')

# options
min_token_length     = int(config.get('Params','TOKEN_LENGTH_THRESHOLD')[0])
restrict_to_letters  = bool(config.get('Params','ONLY_LETTERS')[0])
ignore_stop_words    = bool(config.get('Params','IGNORE_STOP_WORDS')[0])

articles             = OrderedDict()

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

tokens = dt.valmap(index.get_tokens,articles)

index  = index.build_inverted_index(
	tokens            = tokens,
	remove_stop_words = ignore_stop_words,
	count_duplicates  = True,
	min_token_length  = min_token_length,
	only_letters      = restrict_to_letters)

# for debugging purposes only
pickle_dump_file = current_file_location+'/'+'inverted_index_dict_pickle_dump.out'
pickle.dump(index,open(pickle_dump_file,"wb"))

for file in output_files:
	absolute_file = current_file_location+'/'+file
	w             = csv.writer(open(absolute_file,"w"),delimiter=";")

	for key,val in index.iteritems():
		w.writerow([key,val])

log.info("Finished module execution: 'inverted_index'")

