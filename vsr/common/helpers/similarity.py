from scipy import spatial

import numpy as np

def cosine_distance(npvector1,npvector2):
	return(spatial.distance.cosine(npvector1,npvector2))

def get_position(id,doc_distance_pairs):
	idx                               = 1 # 1-indexed

	for pair in doc_distance_pairs:
		doc_id = pair[0]
		if int(doc_id) == int(id):
			return(idx)
		else:
			idx += 1

	# if it's reached here, then given id coudl'nt be found in the results
	raise RuntimeError("Failed to find {0} in query results".format(id))			
