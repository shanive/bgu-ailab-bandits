#! /usr/bin/python
from math import sqrt
from math import exp

num_of_Cps = 9
min_samples = 10
sample_step = 2


"""this program reads results of the cp experiment from log file and computes the best cp value"""

def serialCp(n):
	"""compute value of cp in the geometric series 0.125*sqrt(2)**n"""
	return 0.125*sqrt(2)**n

def readLogFiles():
	"""read results of cp experiment from files.
	return results table"""
	cps = [serialCp(n) for n in range(num_of_Cps)]
	results = []
	for cp in cps:
		lines = open("uniform-uct-Cp="+str(cp)+".log").readlines()[1:] #first line doen't include results
		col = [float(line.split()[2]) for line in lines] #for every number of samples, saves the result of UCT
		results.append(col)
	return results

def bestCp(medians):
	"""receive list of results' median and return the best cp value"""
	best_cp_indx = 0
	for i in range(1, num_of_Cps):
		if medians[best_cp_indx]<medians[i]:
			best_cp_indx = i
	return serialCp(best_cp_indx)	

def printResults(results, medians, bestcp):
	"""printer"""
	#first row:
	print "%-10s" % "samples",
	for n in range(num_of_Cps):
		print "%-10f" % serialCp(n),
	print
	global min_samples
	global sample_step
	samples = min_samples
	for i in range(len(results[0])):
		print "%-10d" % samples,
		for j in range(num_of_Cps):
			print  "%-10f" % results[j][i],
		print
		samples *= sample_step
	#last row:
	print "%-10s" % "median",
	for i in range(num_of_Cps):
		print "%-10f" % medians[i],
	print
	print "The best cp is: %f" % bestcp 

	

def compute(results):
	"""receive UCT results for every cp value
	print statistics"""
	medians = []
	for cp_res in results:
		sort_cp_res = cp_res[:]
		sort_cp_res.sort() #copy results and sort it
		n = len(sort_cp_res)
		if n % 2 == 0:
			med = (sort_cp_res[n/2 - 1] + sort_cp_res[n/2])/2.0
		else:
			med = sort_cp_res[n/2]
		medians.append(med)
	bestcp = bestCp(medians)
	printResults(results, medians, bestcp)
	  
		 

	 
		
		
	
if __name__ == "__main__":
	results = readLogFiles()
	compute(results) 
