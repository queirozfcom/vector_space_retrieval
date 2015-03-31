from vsm.common.classes import MultiOrderedDict
from xml.dom.minidom import parse, parseString

import os
import ConfigParser

current_file_location = os.path.dirname(os.path.realpath(__file__))
config_filename = current_file_location+'/gli.cfg'
config_section = 'Steps'

# what files should I read?
config = ConfigParser.RawConfigParser(dict_type=MultiOrderedDict)

config.read(config_filename)

files_to_read = config.get('Steps','LEIA')

print(files_to_read)