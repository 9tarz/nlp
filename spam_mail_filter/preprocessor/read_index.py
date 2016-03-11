import os
import multiprocessing
def run_shell(index):
	type = index[0]
	i = index[1]
	if (type == "spam"):
		cmd = "mv ../output_1/inmail."+ str(i) + ".json" + " " + "../spam/inmail."+ str(i) + ".json"
		#print cmd
	elif (type == "ham"):
		cmd = "mv ../output_1/inmail."+ str(i) + ".json" +  " " + "../ham/inmail."+ str(i) + ".json"
	else :
		cmd = ""
	os.system(cmd)

def read_index_file(path):
	lines = [line.rstrip('\n') for line in open(path)]
	out = []
	for line in lines:
		element = line.split(' ')
		path = element[1].split(".")
		pack = [element[0],path[3]]
		out.append(pack)
	return out

if __name__ == '__main__' :
	index_path = "../../trec07p/full/index"
	index = read_index_file(index_path)
	
	#pool = multiprocessing.Pool(multiprocessing.cpu_count())
	#pool.map(run_shell, index[0:13])
	#pool.map(run_shell, range(1,2))



