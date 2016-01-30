import nltk
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from Queue import Queue
from threading import Thread
lmtzr = WordNetLemmatizer()
path = "food_and_drink-pages/"
list = []
from nltk.corpus import wordnet

def words_lemmatizer(i):
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
	print str(i) + " finished!"

class MyThread(Thread):
    def __init__(self, i):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.i = i
 
    def run(self):
        words_lemmatizer(self.i)


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

for i in range(1,1171): #1171
	MyThread(i).start()

out = Counter(list)
out_sort = out.most_common()
for (word,count) in out_sort :
	print word.encode("utf8") + " : " + str(count) 
