from vsr.modules.inverted_index.main import run as run_inverted_index
from vsr.modules.indexer.main import run as run_indexer
from vsr.modules.query_processor.main import run as run_query_processor
from vsr.modules.search.main import run as run_search
from vsr.modules.metrics.main import run as run_metrics

import ConfigParser
import os
import time

# This function is called when this file is run as a python module, i.e.
#   when users run python -m vsr.main
def run_all_modules(global_params):

    start_time = time.time()
    
    run_inverted_index(override_params = global_params)
    run_indexer(override_params = global_params)
    run_query_processor(override_params = global_params)
    run_search(override_params = global_params)
    run_metrics(override_params = global_params)

    elapsed_time = time.time() - start_time

    print("Total elapsed time: {0}".format(elapsed_time))

# load global params from global config file
if __name__ == "__main__":

    config_file                      = 'global.cfg'
    current_file_location            = os.path.dirname(os.path.realpath(__file__))
    config_file_absolute             = current_file_location+'/'+config_file
    config                           = ConfigParser.ConfigParser()
    config.read(config_file_absolute)

    params                           = dict()

    params['USE_STEMMER']            = config.getboolean('Params','USE_STEMMER')
    params['TOKEN_LENGTH_THRESHOLD'] = config.getint('Params','TOKEN_LENGTH_THRESHOLD')
    params['ONLY_LETTERS']           = config.getboolean('Params','ONLY_LETTERS')
    params['IGNORE_STOP_WORDS']      = config.getboolean('Params','IGNORE_STOP_WORDS')

    run_all_modules(params)
           