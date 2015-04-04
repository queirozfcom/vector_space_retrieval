
def validate_weight_function(param):
	available_options = ['tf-idf']
	if not param in available_options:
		raise ValueError("Invalid weighting function. Available values are {0}".format(available_options))

def validate_positive_integer(param):
	if isinstance(param,int) and (param > 0):
		return(None)
	else:	
		raise ValueError("Invalid value, expected positive integer, got {0}".format(param)) 
