from vsm.common.classes import MultiOrderedDict
from vsm.common.helpers.dom import get_contents,get_index
from xml.dom import minidom

import ConfigParser
import os
import resource

config_file = 'gli.cfg'
config_section = 'Steps'

current_file_location = os.path.dirname(os.path.realpath(__file__))

config_file_absolute = current_file_location+'/'+config_file

config = ConfigParser.RawConfigParser(dict_type=MultiOrderedDict)
config.read(config_file_absolute)

input_files  = config.get('Steps','LEIA')
output_files = config.get('Steps','ESCREVA')

all_articles = dict()

for file in input_files:
	absolute_file = current_file_location+'/'+file
	xmldoc = minidom.parse(absolute_file)
	
	for record in xmldoc.getElementsByTagName("RECORD"):

		index = get_index(record)
		try:
			contents = get_contents(record)
		except RuntimeError:
			continue

		all_articles[index] = contents


res = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

print(res)