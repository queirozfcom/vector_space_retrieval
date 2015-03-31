from ..common.classes import MultiOrderedDict

import ConfigParser

from xml.dom.minidom import parse, parseString

config_filename = 'gli.cfg'
config_section = ''

# what files should I read?
config = ConfigParser.ConfigParser()

config.read(config_filename)

files_to_read = config.get('LEIA')

