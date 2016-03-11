import os
import multiprocessing
def run_shell(i):
	cmd = "cat ../trec07p/data/inmail." + str(i) + "| node parse_email.js > output_1/inmail." + str(i) + ".json"
	os.system(cmd)

if __name__ == '__main__' :
	pool = multiprocessing.Pool(multiprocessing.cpu_count())
	pool.map(run_shell, range(1,75419))
	#pool.map(run_shell, range(1,2))



