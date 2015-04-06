def validate_positive_integer(param):
	if isinstance(param,int) and (param > 0):
		return(None)
	else:	
		raise ValueError("Invalid value, expected positive integer, got {0}".format(param)) 
