import sys
import matplotlib.pyplot as plt

def readResults(filename):
	"""reads results of experinent from a given file 
	returns tuple of results"""
	pulls = []
	regret = []
	resultfile = open(filename, 'r')
	 
	for line in resultfile:
		templist = line.split()
		pulls.append(templist[0])
		regret.append(templist[1])
	resultfile.close()
	
	#first row is "sampls-regret"
	pulls = pulls[1:]
	regret = regret[1:]
	#convert pulls to int
	pulls = [int(x) for x in pulls]
	#convert regret to float
	regret = [float(y) for y in regret]
		 
	return (pulls, regret)
	
if __name__ == '__main__':
	arrays = readResults(sys.argv[1])
	plt.plot(arrays[0], arrays[1])
	plt.xlabel('samples')
	plt.ylabel('regret')
	plt.savefig(sys.argv[2])
	
	
	
	
	
	
	