from __future__ import division
import sys, os, lucene
from xml.dom import minidom

# helpers
from vsr.common.helpers import dom,logger
from vsr.modules.pylucene.helpers import index as index_helper 



# java stuff    
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField, IntField
# from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

def run():
    current_file_location = os.path.dirname(os.path.realpath(__file__))
    log         = logger.init_log(current_file_location+'/../../../logs/vsr.log',mode='w')
    log.info("Started module execution: 'pylucene'")

    lucene.initVM()
    
    INDEX_DIR   = '/tmp/lucene-index'
    
    files       = [
    "../../../data/cf74.xml",
    "../../../data/cf75.xml",
    "../../../data/cf76.xml",
    "../../../data/cf77.xml",
    "../../../data/cf78.xml",
    "../../../data/cf79.xml"]

    index_helper.index_files(INDEX_DIR, log=log, input_files = files)       

    doc_ids = index_helper.search_abstract(INDEX_DIR,"What are the effects of calcium on the physical properties of mucus from CF patients?",log)

    print(doc_ids[:10])


    log.info("Finished module execution: 'pylucene'")
    print("Finished module execution: 'pylucene'")


if __name__ == "__main__":
    run()            