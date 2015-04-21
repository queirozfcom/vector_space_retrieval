from collections import OrderedDict

import csv
import sys

# returns an ordered dict[int,list[int]]
def load_from_csv_file(path_to_file):
	# ordered dict so as to keep the same order and avoid 'surprises'
	data = OrderedDict()

	with open(path_to_file,'r') as csvfile:
		reader = csv.reader(csvfile,delimiter=';')

		for row in reader:
			query_id       = row[0].strip()
			document_ids   = map(lambda str: int(str.strip("'")), 
				row[1].lstrip('[').rstrip(']').split(','))

			data[query_id] = document_ids

	return(data)		 

def write_to_csv_file(model,output_file):

	if isinstance(model,list):
		a_dict = OrderedDict()
		for lst in model:
			a_dict[lst[0]] = lst[1]
		model = a_dict	

	with open(output_file,"w") as outfile:
		w = csv.writer(outfile,delimiter=';')

		for key,vals in model.iteritems():
			w.writerow([key,vals])


