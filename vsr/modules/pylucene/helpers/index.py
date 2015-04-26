from __future__ import division
import sys, os, lucene
from xml.dom import minidom

# helpers
from vsr.common.helpers import dom

# java stuff    
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, IntField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

# search stuff only
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

def index_files(path,log,input_files):



    directory   = _get_store(path)
        
    
    analyzer    = _get_analyzer()
    
    # analyzer  = LimitTokenCountAnalyzer(analyzer, 10000)

    config      = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer      = IndexWriter(directory, config)

     
    current_file_location = os.path.dirname(os.path.realpath(__file__))

    for file in input_files:
        absolute_file       = current_file_location+'/'+file
        xmldoc              = minidom.parse(absolute_file)
        
        records             = xmldoc.getElementsByTagName("RECORD")

        for record in records:

            record_num = dom.get_num(record)

            try:
                contents = dom.get_contents(record)
            except RuntimeError:
                log.warning("Found article with no contents ({0}); not adding to lucene index.".format(record_num))
                continue # couldn't find article contents, skip
           
            doc = Document()
            doc.add(IntField("doc_id",record_num,Field.Store.YES))
            doc.add(TextField("abstract",contents,Field.Store.NO))

            writer.addDocument(doc)
        

    writer.commit()

    doc_count = writer.numDocs()

    writer.close()
    log.info("Finished building lucene index at {0} with {1} documents".format(path,doc_count))

# Searches the given lucene index using given query and return a list of document_ids, ranked from
#  highest to lowest scoring
def search_abstract(path_to_index,query,log):
    
    analyzer      = _get_analyzer()
    store         = _get_store(path_to_index)
    searcher      = IndexSearcher(DirectoryReader.open(store))

    log.info("Opened a lucene index at {0} for reading".format(path_to_index))

    query_parser  = QueryParser(Version.LUCENE_CURRENT, "abstract", analyzer)
    parsed_query  = query_parser.parse(query)

    docs          = searcher.search(parsed_query,500).scoreDocs

    doc_ids       = list()

    for i,hit in enumerate(docs):
        doc    = searcher.doc(hit.doc)

        # this is the doc_id that I indexed, not the one lucene gave the doc
        doc_id = doc.get("doc_id")
        doc_ids.append(doc_id)

    return(doc_ids)   

def _get_analyzer():
    analyzer    = StandardAnalyzer(Version.LUCENE_CURRENT)
    return(analyzer)                   

def _get_store(path):
    store = SimpleFSDirectory(File(path))   
    return(store) 