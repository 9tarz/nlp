import nltk
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
path = "food_and_drink-pages/"
list = []
from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):
	if treebank_tag.startswith('J'):
		return wordnet.ADJ
	elif treebank_tag.startswith('V'):
		return wordnet.VERB
	elif treebank_tag.startswith('N'):
		return wordnet.NOUN
	elif treebank_tag.startswith('R'):
		return wordnet.ADV
	else:
		return ''

for i in range(1,1171):
	file_content = open(path + str(i) + ".txt").read()
	data = file_content.decode("utf8")
	tokens = nltk.word_tokenize(data)
	tokens_pos = nltk.pos_tag(tokens)
	for (token,pos) in tokens_pos :
		if get_wordnet_pos(pos) == '' :
			list.append(token)
		else :
			word_lmtz = lmtzr.lemmatize(token,get_wordnet_pos(pos))
			#print token + " : "+ word_lmtz + ": " + get_wordnet_pos(pos)
			list.append(word_lmtz)

out = Counter(list)
out_sort = out.most_common()
for (word,count) in out_sort :
	print word.encode("utf8") + " : " + str(count) 
