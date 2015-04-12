import time

start_time = time.time()

import vsr.inverted_index.main
import vsr.indexer.main
import vsr.query_processor.main
import vsr.search.main
import vsr.metrics.main

elapsed_time = time.time() - start_time

print("Total elapsed time: {0}".format(elapsed_time))