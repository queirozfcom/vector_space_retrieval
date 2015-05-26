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
    ACTUAL_RESULTS_FILE   = current_file+'/../search/output/actual_results_only_doc_ids.csv'

    lucene_helper.index_files(INDEX_DIR, log=log, input_files = INPUT_FILES)       

    # an ordered dict mapping query_ids to document_ids
    expected_results      = results_helper.load_from_csv_file(EXPECTED_RESULTS_FILE)

    # an ordered dict mapping query ids to query texts
    raw_queries           = results_helper.load_from_csv_file(RAW_QUERIES_FILE)
    tokenized_queries     = OrderedDict()

    for query_id,query_text in raw_queries.iteritems():
        tokenized_queries[query_id] = lucene_helper.tokenize_query(query_text)


    # a dict mapping query_ids to document_ids (same structure as above)
    actual_results         = results_helper.load_from_csv_file(ACTUAL_RESULTS_FILE)
    actual_results_lu      = lucene_helper.search_abstracts(INDEX_DIR,raw_queries, log)


    # calculating the same metrics that we did before (under module 'metrics')
    precisions_lu          = precision.calculate(expected_results,actual_results_lu)
    recalls_lu             = recall.calculate(expected_results,actual_results_lu)
    f1_scores_lu           = f_score.calculate(expected_results,actual_results_lu,beta=1)
    mean_ap_value_lu       = mean_ap.calculate(expected_results,actual_results_lu)    
    precisions_at_10_lu    = precision.calculate(expected_results,actual_results_lu,threshold=10)

    # so we can compare both in a graph
    precision_11_points    = precision.calculate_points(expected_results,actual_results)
    precision_11_points_lu = precision.calculate_points(expected_results,actual_results_lu)

    # tokenized queries so that possible code reviewers can see what's going on
    results_helper.write_to_csv_file(tokenized_queries,OUTPUT_DIRECTORY+'tokenized_queries.csv')

    # the results using lucene. They're displayed in the same format as the results from other
    # modules, so we can easily compare the performance of both
    results_helper.write_to_csv_file(actual_results_lu,OUTPUT_DIRECTORY+'search_results_only_doc_ids.csv')

    # metrics for this module
    results_helper.write_to_csv_file(precisions_lu,OUTPUT_DIRECTORY+'precisions_lucene.csv')
    results_helper.write_to_csv_file(recalls_lu,OUTPUT_DIRECTORY+'recalls_lucene.csv')
    results_helper.write_to_csv_file(f1_scores_lu,OUTPUT_DIRECTORY+'f1_scores_lucene.csv')
    results_helper.write_to_csv_file(precisions_at_10_lu,OUTPUT_DIRECTORY+'precisions_at_10_lucene.csv')
    results_helper.write_to_csv_file(precision_11_points_lu,OUTPUT_DIRECTORY+'precision_11_points_lucene.csv')

    # mean_ap is a single number
    with open(OUTPUT_DIRECTORY+'mean_ap_lucene.txt','w') as outfile:
        outfile.write(str(mean_ap_value_lu))

    plot_helper.plot_recall_precision_curve(
        precision_11_points_lu,
        title = "Precision-Recall curve (using EnglishAnalyzer on Lucene)",
        display = False,
        color   = 'r',
        filename = OUTPUT_DIRECTORY+'precision_11_points_lucene.png' )

    plot_helper.plot_merged_recall_precision_curve(
        precision_11_points,
        precision_11_points_lu,
        colors = ['b','r'],
        titles = ["Hand-coded indexing and searching","Using Lucene's EnglishAnalyzer"],
        display = False,
        filename=OUTPUT_DIRECTORY+'precision_11_points_comparison.png')

    log.info("Finished module execution: 'pylucene'")
    print("Finished module execution: 'pylucene'")


if __name__ == "__main__":
    run()            