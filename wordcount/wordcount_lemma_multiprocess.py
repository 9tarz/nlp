import nltk
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import multiprocessing

lmtzr = WordNetLemmatizer()
path = "food_and_drink-pages/"

def words_lemmatizer(i):
	words_list = []
	file_content = open(path + str(i) + ".txt").read()
	data = file_content.decode("utf8")
	tokens = nltk.word_tokenize(data)
	tokens_pos = nltk.pos_tag(tokens)
	for (token,pos) in tokens_pos :
		if get_wordnet_pos(pos) == '' :
			words_list.append(token)
		else :
			word_lmtz = lmtzr.lemmatize(token,get_wordnet_pos(pos))
			#print token + " : "+ word_lmtz + ": " + get_wordnet_pos(pos)
			words_list.append(word_lmtz)

	return words_list

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

if __name__ == '__main__' :
	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	lists = pool.map(words_lemmatizer, range(1,1171))
	lists = [word for words_list in lists for word in words_list]
	out = Counter(lists)
	out_sort = out.most_common()
	for (word,count) in out_sort :
		print word.encode("utf8") + " : " + str(count) 

