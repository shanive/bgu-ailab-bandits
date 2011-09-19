"""this module contain an experiment on sos game"""

import sys
import sosGame
import getopt
import sosAgents
from random import choice

def usage():
	"""print usage message to standart output"""
	print "Usage: python sosTest.py --min min-n --max max-n --step step-n --repeat reapetions --order r/a/d --white white-name --black black-name"  
 
def inputParser(argList):
	"""receive input for SOS Game experiment"""
	### default values:
	minN = 10
	maxN = 1000
	step = 2
	repetitions = 100000
	order = 'r'	 #'r' = random, 'a' = ascending, 'd' = descending)  
	white = 'random'
	black = 'random'
	
	try:
		opts, args = getopt.getopt(argList,"",["min=","max=","step=", "repeat=", "order=", "white=", "black="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	for opt,arg in opts:
		if opt == '--min':
			minN = int(arg)
		elif opt == '--max':
			maxN = int(arg)
		elif opt == '--step':
			step = float(arg)
		elif opt == '--repeat':
			repetitions = int(arg)
		elif opt == '--order' and arg in ('r','a','d'):
			order = arg
		elif opt == '--white' and arg in ('random', 'uniform', 'left', 'right'):
			white = arg
		elif opt == '--black' and arg in ('random', 'uniform', 'left', 'right'):
			black = arg
		else:
			print "Unvalid Option\n"
			usage()
			sys.exit(2)  
			
 	sosExperiment(minN, maxN, step, repetitions, order, white, black)
 		
def sosExperiment(minN, maxN, step, repetitions, order, white, black):
	"""excecute the experiment and prints results"""
	res = [["n"],["difference"]]
	###print first row in results table:
	print "%-10s %-10s\n" % ("n", "difference")
	
	whitePlayer = getattr(sosAgents, white)
	blackPlayer = getattr(sosAgents, black)
	
	game = sosGame.SOSGame(whitePlayer, blackPlayer, minN, order)
	n = minN
	while n <= maxN:
		game.changeSize(n, order)
		avgDiff = 0.0	
		for reapet in range(repetitions):
			avgDiff += game.newGame()
		avgDiff = avgDiff / repetitions
		
		res[0].append(n)
		res[1].append(avgDiff)
		###print row in results table:
		print "%-10d %-10f\n" % (n, avgDiff)
		
		n = n * step
		if round(n) > n:
			n = int(round(n) - 1)
		else:
			n = int(round(n))	
		
	#printResults(res)
	
#def printResults(results):
	
	#strToPrint = ""
	#strToPrint = "%-10s %-10s\n" % (results[0][0], results[1][0])
	#for row in range(1, len(results[0])):
		#strToPrint += "%-10d %-10f\n" % (results[0][row], results[1][row])
	#print strToPrint
		
if __name__ == '__main__':
	inputParser(sys.argv[1:])
	
	
