import logging as log

def init_log(path_to_file,mode='a'):
	FORMAT='%(asctime)s %(levelname)s: %(message)s'
	DATEFMT='%d %b %H:%M:%S'
	log.basicConfig(
		filename=path_to_file,
		level=log.DEBUG, 
		format=FORMAT,datefmt=DATEFMT,
		filemode=mode) # append to previous log

	return(log)