from nltk.tokenize import word_tokenize

# dict should be a dictionary with identifiers as keys and a list of tokens
# as value
def build_inverted_index(tokens,count_duplicates=False):
	index = dict()
	for key,token_list in tokens.iteritems():
		
		token_list_upper = map(lambda x: x.upper(), token_list)

		for token_upper in set(token_list_upper):

			if not token_upper.isalpha():
				continue

			if token_upper not in index:
				index[token_upper] = list()

			if(count_duplicates):	
				for i in range(token_list_upper.count(token_upper)):
					index[token_upper].append(key) # as many times as it appears				
			else:
				index[token_upper].append(key) # just once

	return(index)			

def get_tokens(text):
	return(word_tokenize(text))	
