def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def merge_params(params,overrides):

	if overrides is None:
		return(params)
	else:
		for key,val in overrides.iteritems():
			params[key] = val

		return(params)	
