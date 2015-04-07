from collections import OrderedDict
from pprint import pprint
from scipy import spatial
from vsr.common.helpers.similarity import(
    get_position,
    cosine_distance)
from xml.dom import minidom

import ConfigParser
import csv
import logging as log
import numpy as np
import os
import resource
import sys

current_file_location = os.path.dirname(os.path.realpath(__file__))

log_file = '../../logs/vsr.log'
FORMAT   = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT  = '%d %b %H:%M:%S'
log.basicConfig(
    filename=current_file_location+'/'+log_file,
    level=log.DEBUG, 
    format=FORMAT,datefmt=DATEFMT,
    filemode='a') # append to existing file

log.info("Started module execution: 'search'")

config_file                  = 'busca.cfg'
config_file_absolute         = current_file_location+'/'+config_file

config                       = ConfigParser.ConfigParser()
config.read(config_file_absolute)

# input files (queries and documents modelled in the same space)
document_model_file          = config.get('InputFiles','MODELO')
query_model_file             = config.get('InputFiles','CONSULTAS')

# output files
actual_results_file          = config.get('OutputFiles','RESULTADOS')

document_model_file_absolute = current_file_location+'/'+document_model_file
query_model_file_absolute    = current_file_location+'/'+query_model_file


# LOAD QUERY MODEL INTO MEMORY

queries_dict                 = OrderedDict()

with open(query_model_file_absolute, 'rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=';')
    for row in reader:
        query_id = int(row[0])
        token_vector = row[1].lstrip('[').rstrip(']').split(',')
        # store stuff as nparray so i dont have to convert at query time
        queries_dict[query_id] = np.asarray(map(float,token_vector))




# LOAD DOCUMENT MODEL INTO MEMORY

docs_dict                    = OrderedDict()


with open(document_model_file_absolute , 'rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=';')
    for row in reader:
        doc_id = int(row[0])
        token_vector = row[1].lstrip('[').rstrip(']').split(',')
        # store stuff as nparray so i dont have to convert at query time
        docs_dict[doc_id] = np.asarray(map(float,token_vector))
    



# WORK OUT RESULTS

results_dict                              = OrderedDict()

actual_results_file_absolute              = current_file_location + '/' + actual_results_file 

actual_results_doc_ids_only               = actual_results_file.replace('.csv','_only_doc_ids.csv')
actual_results_file_doc_ids_only_absolute = current_file_location+'/'+actual_results_doc_ids_only

w_actual_results                          = csv.writer(open(actual_results_file_absolute,"w"),delimiter=";")
w_actual_results_doc_ids_only             = csv.writer(open(actual_results_file_doc_ids_only_absolute,"w"),delimiter=";")



# one result line per query
for query_id,query_vector in queries_dict.iteritems():
    results_row                   = list()
    results_row.append(query_id)

    doc_distance_pairs            = list()

    for doc_id,doc_vector in docs_dict.iteritems():

        distance   = cosine_distance(query_vector,doc_vector)
        doc_distance_pairs.append([doc_id,distance])      

    # this is the way data will be written to the csv file    
    position_doc_distance_triples = list()

    sorted_doc_distance_pairs     = sorted(doc_distance_pairs,key = lambda elem: elem[1])


    for i,pair in enumerate(sorted_doc_distance_pairs, start = 1):
       doc_id     = pair[0]
       distance   = pair[1]

       # 1-indexed
       position   = i

       if(float(distance) == 1.0):
           continue
                       
       position_doc_distance_triples.append([position,doc_id,round(distance,3)])

    # highest score first so we can compare more easily with the expect results
    sorted_doc_distance_pairs     = sorted(position_doc_distance_triples,key = lambda elem: elem[0]) 

    results_row.append(position_doc_distance_triples)

    # one result line per query
    w_actual_results.writerow(results_row)
    w_actual_results_doc_ids_only.writerow([query_id,map(lambda lst: lst[1], position_doc_distance_triples)])


log.info("Finished module execution: 'search'")

