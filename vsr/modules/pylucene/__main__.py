from __future__ import division
from collections import OrderedDict
import sys, os, lucene
from xml.dom import minidom

# helpers
from vsr.common.helpers import dom,logger
from vsr.common.helpers import results as results_helper
from vsr.common.helpers import plot as plot_helper
from vsr.modules.pylucene.helpers import index as lucene_helper 
from vsr.modules.metrics.measures import f_score, mean_ap, precision, recall

# java stuff    
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField, IntField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

def run():
    current_file = os.path.dirname(os.path.realpath(__file__))
    log          = logger.init_log(current_file+'/../../../logs/vsr.log',mode='w')
    log.info("Started module execution: 'pylucene'")

    lucene.initVM()
        
    INDEX_DIR   = '/tmp/lucene-index'
    INPUT_FILES = [
    "../../../data/cf74.xml",
    "../../../data/cf75.xml",
    "../../../data/cf76.xml",
    "../../../data/cf77.xml",
    "../../../data/cf78.xml",
    "../../../data/cf79.xml"]
    EXPECTED_RESULTS_FILE = current_file+'/../query_processor/output/expected_query_results_only_doc_ids.csv'   
    RAW_QUERIES_FILE      = current_file+'/../query_processor/output/raw_queries.csv'
    OUTPUT_DIRECTORY      = current_file+'/output/'

    lucene_helper.index_files(INDEX_DIR, log=log, input_files = INPUT_FILES)       

    # an ordered dict mapping query_ids to document_ids
    expected_results      = results_helper.load_from_csv_file(EXPECTED_RESULTS_FILE)

    # an ordered dict mapping query ids to query texts
    raw_queries           = results_helper.load_from_csv_file(RAW_QUERIES_FILE)
    tokenized_queries     = OrderedDict()

    for query_id,query_text in raw_queries.iteritems():
        tokenized_queries[query_id] = lucene_helper.tokenize_query(query_text)


    # a dict mapping query_ids to document_ids (same structure as above)
    actual_results        = lucene_helper.search_abstracts(INDEX_DIR,raw_queries, log)

    # calculating the same metrics that we did before (under module 'metrics')
    precisions            = precision.calculate(expected_results,actual_results)
    recalls               = recall.calculate(expected_results,actual_results)
    f1_scores             = f_score.calculate(expected_results,actual_results,beta=1)
    mean_ap_value         = mean_ap.calculate(expected_results,actual_results)    
    precisions_at_10      = precision.calculate(expected_results,actual_results,threshold=10)
    precision_11_points   = precision.calculate_points(expected_results,actual_results)

    # tokenized queries so that possible code reviewers can see what's going on
    results_helper.write_to_csv_file(tokenized_queries,OUTPUT_DIRECTORY+'tokenized_queries.csv')

    # the results from using lucene. They're displayed in the same format as the results from other
    # modules, so we can easily compare the performance of both
    results_helper.write_to_csv_file(actual_results,OUTPUT_DIRECTORY+'search_results_only_doc_ids.csv')

    # metrics for this module
    results_helper.write_to_csv_file(precisions,OUTPUT_DIRECTORY+'precisions.csv')
    results_helper.write_to_csv_file(recalls,OUTPUT_DIRECTORY+'recalls.csv')
    results_helper.write_to_csv_file(f1_scores,OUTPUT_DIRECTORY+'f1_scores.csv')
    results_helper.write_to_csv_file(precisions_at_10,OUTPUT_DIRECTORY+'precisions_at_10.csv')
    results_helper.write_to_csv_file(precision_11_points,OUTPUT_DIRECTORY+'precision_11_points.csv')

    # mean_ap is a single number
    with open(OUTPUT_DIRECTORY+'mean_ap.txt','w') as outfile:
        outfile.write(str(mean_ap_value))

    plot_helper.plot_recall_precision_curve(
        precision_11_points,
        title = "Precision-Recall curve (using EnglishAnalyzer on Lucene)",
        display = False,
        filename = OUTPUT_DIRECTORY+'precision_11_points.png' )

    log.info("Finished module execution: 'pylucene'")
    print("Finished module execution: 'pylucene'")


if __name__ == "__main__":
    run()            