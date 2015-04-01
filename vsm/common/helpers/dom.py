def get_index(record_node):
	maybe_recordnums = record_node.getElementsByTagName("RECORDNUM")

	if(len(maybe_recordnums)==0):
		raise RuntimeError("Node must have 'RECORDNUM' subnode!")
	elif(len(maybe_recordnums) != 1):
		raise RuntimeError("Node must have only one 'RECORDNUM' subnode!")
	else:
		return(maybe_recordnums[0].firstChild.nodeValue)	

def get_contents(record_node):
	node_index = get_index(record_node)
	maybe_abstracts = record_node.getElementsByTagName("ABSTRACT")
	maybe_extracts  = record_node.getElementsByTagName("EXTRACT")

	if(len(maybe_extracts) == 0 and len(maybe_abstracts) ==0):	
		raise RuntimeError("Node ",node_index," has neither 'EXTRACT' nor 'ABSTRACT' subnodes!")	
	elif(len(maybe_extracts) != 0 and len(maybe_abstracts) != 0):
		raise RuntimeError("Node ",node_index," must have only one of the following subnodes: 'EXTRACT','ABSTRACT'!")
	elif(len(maybe_extracts) == 0 and len(maybe_abstracts) != 0 ):
		return(maybe_abstracts[0])
	elif(len(maybe_extracts) != 0 and len(maybe_abstracts) == 0):
		return(maybe_extracts[0])	