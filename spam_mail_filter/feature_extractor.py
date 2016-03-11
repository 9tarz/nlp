import json
import nltk
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import multiprocessing as mp
from nltk.corpus import stopwords
import string
import re
import operator
import math
import collections

lmtzr = WordNetLemmatizer()
q_spam = mp.Queue()
q_ham = mp.Queue()
stops = set(stopwords.words('english'))
stops_add = set(["'d", "'ll", "'m", "'re", "'s", "'t", "n't", "'ve"])
stops = stops.union(stops_add)
punctuations = set(string.punctuation)
punctuations.add("''")
punctuations.add("``") 
FEATURE_CHARS = set([";","(","!","$","#"])
punctuations_feature_chars = punctuations.difference(FEATURE_CHARS)
stops_punctuations_feature_chars = punctuations_feature_chars.union(stops)
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
	text = text.replace('\n', ' ')
	return TAG_RE.sub('', text)

def read_index_file(path, cond):
	lines = [line.rstrip('\n') for line in open(path)]
	out = []
	for line in lines:
		element = line.split(' ')
		path = element[1].split("/")
		pack = [element[0],path[2]] #element[0]:type, path[3]:path
		if (cond == "spam"):
			if (element[0] == "spam"):
				out.append(pack)
			else:
				pass
		if (cond == "ham"):
			if (element[0] == "ham"):
				out.append(pack)
			else:
				pass
	return out

def read_index_file_all(path):
	lines = [line.rstrip('\n') for line in open(path)]
	out = []
	for line in lines:
		element = line.split(' ')
		path = element[1].split("/")
		pack = [element[0],path[2]] #element[0]:type, path[3]:path
		out.append(pack)
	return out


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

#def words_lemmatizer(index,cond):
def words_lemmatizer(args):
	index = args[0]
	cond = args[1]
	words_list = []
	all_words = []
	file_content = open(index[0]+"/"+index[1]+".json")
	data_json = json.load(file_content)
	try:
		data = data_json["text"]
	except KeyError:
		try:
			data_html = data_json["html"]
			data = remove_tags(data_html)
		except KeyError:
			data = ""
	tokens = [i for i in nltk.word_tokenize(data.lower()) if i not in stops_punctuations_feature_chars]
	tokens_pos = nltk.pos_tag(tokens)
	for (token,pos) in tokens_pos :
		if get_wordnet_pos(pos) == '' :
			all_words.append(token)
			if token not in words_list:
				words_list.append(token)
		else :
			word_lmtz = lmtzr.lemmatize(token,get_wordnet_pos(pos))
			all_words.append(word_lmtz)
			if word_lmtz not in words_list:
				words_list.append(word_lmtz)

	#return words_list
	all_words = Counter(all_words)
	all_words = all_words.most_common()

	if (cond == "spam"):
		q_spam.put((words_list,all_words,index[1],cond))
	if (cond == "ham"):
		q_ham.put((words_list,all_words,index[1],cond))


if __name__ == '__main__' :

	NUM_DOC_SPAM = 10.0
	NUM_DOC_HAM = 10.0
	#ignore words with total freq lower than thresh
	RARE_THRESH = 0.005
	#max distance of spamicity from .5
	SPAMICITY_RADIUS = 0.05
	TOP_K = 10

	index_path = "../trec07p/full/index"
	#index = read_index_file(index_path)
	index_spam_paths = read_index_file(index_path,"spam")
	index_ham_paths = read_index_file(index_path, "ham")

	pool = mp.Pool(mp.cpu_count())
	job_args_spam = [(index_spam_paths[i], "spam") for i in range(int(NUM_DOC_SPAM))]
	pool.map(words_lemmatizer, job_args_spam)
	job_args_ham = [(index_ham_paths[i], "ham") for i in range(int(NUM_DOC_HAM))]
	pool.map(words_lemmatizer, job_args_ham)

	results_spam = [q_spam.get() for p in range(len(job_args_spam))]
	words_results_spam = [word for (words_list,all_words,index,cond) in results_spam for word in words_list]
	all_words_results_spam = [(all_words,index,cond) for (words_list,all_words,index,cond) in results_spam]

	freq_results_spam_counter = Counter(words_results_spam)
	freq_results_spam = freq_results_spam_counter.most_common()

	results_ham = [q_ham.get() for p in range(len(job_args_ham))]
	words_results_ham = [word for (words_list,all_words,index,cond) in results_ham for word in words_list]
	all_words_results_ham = [(all_words,index,cond) for (words_list,all_words,index,cond) in results_ham]

	freq_results_ham_counter = Counter(words_results_ham)
	freq_results_ham = freq_results_ham_counter.most_common()

	words_results_spam_prob = dict() # P(w|S)
	for (word,freq) in freq_results_spam:
		words_results_spam_prob[word] = freq/NUM_DOC_SPAM
	words_results_ham_prob = dict() # P(w|H)
	for (word,freq) in freq_results_ham:
		words_results_ham_prob[word] = freq/NUM_DOC_HAM

	all_words_results_spam.extend(all_words_results_ham)
	all_words_results = all_words_results_spam

	num_of_all_words = 0.0
	for (all_words,index,cond) in all_words_results:
		for (word,tf) in all_words:
			num_of_all_words += tf

	all_words_results_prob = dict()
	for (all_words,index,cond) in all_words_results:
		for (word,tf) in all_words:
			all_words_results_prob[word] = tf/num_of_all_words

	#all_words_results_prob = sorted(all_words_results_prob.items(), key=operator.itemgetter(1), reverse=True)
	#print all_words_results_prob

# P(S|w)
	words_results_predict_prob = dict()
	for (word,freq) in freq_results_spam:
		try :
			diff = abs(words_results_spam_prob[word] - words_results_ham_prob[word])
			spamicity = words_results_spam_prob[word]/(words_results_spam_prob[word] + words_results_ham_prob[word])      
			if abs(spamicity - 0.5)>SPAMICITY_RADIUS and freq>RARE_THRESH:
				words_results_predict_prob[word] = diff
			#words_results_predict_prob[word] = words_results_spam_prob[word]/(words_results_spam_prob[word] + words_results_ham_prob[word])
		except KeyError:
			diff = abs(words_results_spam_prob[word])
			spamicity = words_results_spam_prob[word]/words_results_spam_prob[word]
			if abs(spamicity - 0.5)>SPAMICITY_RADIUS and freq>RARE_THRESH:
				words_results_predict_prob[word] = diff
			#words_results_predict_prob[word] = words_results_spam_prob[word]/words_results_spam_prob[word]

		#words_results_predict_prob[word] = words_results_spam_prob[word]/words_results_all_prob[word]
		#try :
		#	print "Spamicity: " + str(words_results_predict_prob[word]) + " Spam: " + str(words_results_spam_prob[word]) +" Ham: "+ str(words_results_ham_prob[word])
		#except KeyError:
		#	print "Spamicity: " + str(words_results_predict_prob[word]) + " Spam: " + str(words_results_spam_prob[word]) +" Ham: 0"
		#print "Indicate: " + str(words_results_predict_prob[word]) + " All: " + str(words_results_all_prob[word])  
	#words_results_predict_prob = sorted(words_results_predict_prob)

	sorted_words_results_predict_prob = sorted(words_results_predict_prob.items(), key=operator.itemgetter(1), reverse=True)[:TOP_K]
	feature_words = [word for (word,prob) in sorted_words_results_predict_prob]
	#print feature_words

	#index_paths = read_index_file_all(index_path)

	idf = dict()
	for word in feature_words:
		idf[word] = math.log((NUM_DOC_SPAM+NUM_DOC_HAM)/(freq_results_spam_counter[word] + freq_results_ham_counter[word]))
	#print idf

	tfidf = dict()
	for (all_words,index,cond) in all_words_results:
		tfidf[index] = dict()
		for fw in feature_words:
			tfidf[index][fw] = 0 
		for (word,tf) in all_words:
			if word in feature_words:
				tfidf_w = tf*idf[word]
				tfidf[index][word] = tfidf_w
				#for tf_index in tfidf[index]:
				#	fw_tfidf_w[word] = tfidf_w
		tfidf[index][u'zzzzzzztype_of_doc'] = cond

	count = 0
	print "@relation 'spam_ham'"
	for doc in tfidf:
		ordered = collections.OrderedDict(sorted(tfidf[doc].items()))
		if (count == 0):
			#print ','.join(str(v[0]) for v in ordered.items())
			count_attr = 0
			for value in ordered.items():
				if (count_attr == TOP_K):
					print "@attribute " + "class" + " {spam,ham}"
				else:
					print "@attribute " + value[0] + " numeric"
				count_attr+=1
			print "@data"
		else:
			print ','.join(str(v[1]) for v in ordered.items())
		count+=1


















