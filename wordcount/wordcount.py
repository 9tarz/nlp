import nltk
from collections import Counter
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
py.sign_in('nulllnil', '8xr93mz7ra')
path = "food_and_drink-pages/"
list = []
for i in range(1,1171):
	file_content = open(path + str(i) + ".txt").read()
	data = file_content.decode("utf8")
	tokens = nltk.word_tokenize(data)
	for token in tokens :
		list.append(token)

out = Counter(list)
out_sort = out.most_common()
count_list = []
for (word,count) in out_sort :
	#print word.encode("utf8") + " : " + str(count)
	count_list.append(count) 

freq_of_freq = Counter(count_list)
freq_of_freq = freq_of_freq.most_common()
freq_of_freq = sorted(freq_of_freq)

keys = []
values = []

for (count,freq) in freq_of_freq :
	#print str(np.log10(count)) + "," + str(np.log10(freq))
	keys.append(np.log10(count))
	values.append(np.log10(freq))


trace = go.Scatter(
    x = keys,
    y = values,
    mode = 'markers',
    name = 'markers'
)
data = [trace]

# Plot and embed in ipython notebook!
py.iplot(data, filename='scatter-mode')