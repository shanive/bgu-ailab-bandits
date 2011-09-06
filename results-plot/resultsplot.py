import sys
import getopt
import plotCreator

def usage():
	"""prints the usage message"""
	print "Usage: python resultsplot.py --logx <basex> --logy <basey> --labelx <label-string> --labely <label-string> <input-file> <output-file>"
	
def readResults(filename):
	"""reads results of experinent from a given file 
	returns list of algorithms' name and results list"""
	
	resultfile = open(filename, 'r')
	
	lines = resultfile.readlines()
	 
	labels = lines[0].split()
	 
	resultlist = [[label] for label in labels] 
	
	lines = lines[1:]
	 
	for line in lines:
		templist = line.split()
		
		for col in range(len(resultlist)):
				
			resultlist[col].append(float(templist[col]))
		
	resultfile.close()
	
	return resultlist
	
if __name__ == '__main__':
	#default values
	logx = 0
	logy = 0
	labelx = "x"
	labely = "y"
	
	try:
		opts, args = getopt.getopt(sys.argv[1:],"", ["logx=", "logy=", "labelx=", "labely="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '--logx':
			logx = float(arg)
		elif opt == '--logy':
			logy = float(arg)
		elif opt == '--labelx':
			labelx = arg
		elif opt == '--labely':
			labely = arg
	
	plotcreator = plotCreator.PlotCreator() 
	resultlist = readResults(args[0])
	plotcreator.create(resultlist, args[1],logx, logy, labelx, labely)
 	
	
	