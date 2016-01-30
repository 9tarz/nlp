import nltk
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
path = "food_and_drink-pages/"
list = []
for i in range(1,3):
	file_content = open(path + str(i) + ".txt").read()
	data = file_content.decode("utf8")
	tokens = nltk.word_tokenize(data)
	tokens_length = len(tokens)
	ref_position = data.find("See also")
	print ref_position
	print tokens[ref_position:tokens_length]
	print " "
	print " "
