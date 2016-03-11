import nltk
import re
from nltk.util import ngrams
from collections import Counter

def find_count(lst, var):
	c = 0
	for (fgram,count) in lst :
		#tmp = (fgram[0],fgram[1],fgram[2])
		if var == fgram :
			c += count
	return float(c)

path = "all_word_segmented_news.u8"
file_content = open(path+ ".txt").read()
n = 4
file_content = file_content.split("\n")
file_content = [x.replace(" _", "") for x in file_content]
lst = []
for x in file_content:
	words = x.split(" ")
	for word in words:
		lst.append(word)
fourgrams = ngrams(lst, n)
threegrams = ngrams(lst, n-1)
fourgrams = [tuple(word.decode("utf8") for word in words) for words in fourgrams]
threegrams = [tuple(word.decode("utf8") for word in words) for words in threegrams]

out4 = Counter(fourgrams)
count_4_list = out4.most_common()

out3 = Counter(threegrams)
count_3_list = out3.most_common()

for (fgram,count) in count_4_list :
	w3 = (fgram[0],fgram[1],fgram[2])
	w3_count = find_count(count_3_list,w3)
	w3 = ' '.join(fgram)
	#print w3.encode("utf8") + " : " + " count4 "+ str(count) + " count3 "+ str(w3_count) +  " prob " + str(count/w3_count)
	print w3.encode("utf8") + " : " + str(count/w3_count)
	#ans.append((w3,float(count/w3_count)))
	#fgram = ','.join(fgram)
	#print fgram.encode("utf8") + " : [" + str(count) + "]"



