from collections import OrderedDict

import csv,re,sys

# returns an ordered dict[int,list[int]]
def load_from_csv_file(path_to_file):
	# ordered dict so as to keep the same order and avoid 'surprises'
	data = OrderedDict()

	with open(path_to_file,'r') as csvfile:
		reader = csv.reader(csvfile,delimiter=';')

		for row in reader:
			query_id       = row[0].strip()

			if _is_python_list(row[1]):
				# doc ids
				value = map(lambda str: int(str.strip("'")), 
					row[1].lstrip('[').rstrip(']').split(','))
			elif _is_python_string(row[1]):
				# just a string
				value = row[1].strip()
			else:
				raise RuntimeError("Csv file at '{0}' does not fit expected structure for parsing".format(path_to_file))	

			data[query_id] = value

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

def _is_python_list(str_representation):
	no_of_open_sq_brackets  = str_representation.count('[')
	no_of_close_sq_brackets = str_representation.count(']')

	if no_of_close_sq_brackets == no_of_open_sq_brackets and (no_of_open_sq_brackets != 0):
		return(True)
	else:
		return(False)	

def _is_python_string(str_representation):
	if _is_python_list(str_representation):
		return(False)
	else:
		return(True)	



