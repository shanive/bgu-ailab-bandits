import sys
import matplotlib.pyplot as plt
import getopt
import matplotlib.axes

def usage():
	"""prints the usage message"""
	print "Usage: python resultsplot.py --logx <basex> --logy <basey> <input-file> <output-file>"
	
def readResults(filename):
	"""reads results of experinent from a given file 
	returns list of algorithms' name and results list"""
	
	resultfile = open(filename, 'r')
	
	lines = resultfile.readlines()
	 
	firstline = lines[0].split()
	 
	resultlist = [[] for col in firstline] 
	
	columns = len(resultlist)
	 
	for line in lines[1:]:
		templist = line.split()
		
		for col in range(columns):
			
			resultlist[col].append(float(templist[col]))
		
	resultfile.close()
	##convert samples to int
	#resultlist[0] = [int(x) for x in resultlist[0]]
	##convert regret to float
	#for i in range(1, columns):
		#resultlist[i] = [float(x) for x in resultlist[i]]
	
	return (firstline[1:],resultlist)
	
if __name__ == '__main__':
	
	logx = 0
	logy = 0
	
	linestyle = ('k-', 'k--', 'k-.', 'k:', 'ko', 'k^', 'kv') 
	
	try:
		opts, args = getopt.getopt(sys.argv[1:],"", ["logx=", "logy="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '--logx':
			logx = float(arg)
		elif opt == '--logy':
			logy = float(arg)
 	
	algonames, resultlist = readResults(args[0])
	plots = len(algonames) 
	
	#if logx and logy:
		#plotFunc = getattr(plt, "loglog")
	#elif logx:
		#plotFunc = getattr(plt, "semilogx")
	#else:
		#plotFunc = getattr(plt, "semilogy")
	
	for plot in range(plots):
		plt.plot(resultlist[0], resultlist[plot + 1], linestyle[plot], label = algonames[plot])
		
	if logx > 1:
		plt.gca().set_xscale('log', basex = logx)
	if logy > 1:
		plt.gca().set_yscale('log', basey = logy)		
		
	plt.xlabel('samples')
	plt.ylabel('regret')
	plt.legend()
	plt.savefig(args[1])
	
	