"""this module contain an experiment on sos game"""

import sys
import model
import getopt
import agents
from random import choice

def pairs(lst):
	"""some"""
	n = len(lst)
	newlst = []
	for i in range(n):
		newlst.append((lst[i],lst[(i+1)%n]))
		newlst.append((lst[(i+1)%n],lst[i]))
	return newlst
    


def usage():
	"""print usage message to standart output"""
	print "Usage: python tournament.py --min min-n --max max-n --step step-n --repeat reapetions --order r/a/d --samples sample-num player-name [player-name]..."
	
def inputParser(argList):
	"""receive input for SOS Game experiment"""
	### default values:
	minN = 10
	maxN = 1000
	step = 2
	repetitions = 100000
	order = 'r'	 #'r' = random, 'a' = ascending, 'd' = descending)  
	#white = 'random'
	#black = 'random'
	samples = 100	##### for MCST algorithm
	
	try:
		opts, args = getopt.getopt(argList,"",["min=","max=","step=", "repeat=", "order=", "samples="])
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
		elif opt == '--samples':
			samples = arg			
		else:
			print "Unvalid Option\n"
			usage()
			sys.exit(2)  
			
 	sosExperiment(minN, maxN, step, repetitions, order, samples, args)
 		
def sosExperiment(minN, maxN, step, repetitions, valorder, samples, players):
	
	pairList = pairs(players)
	res = [["n"]]
	
	firstRow = "%s\t" % "n"
	"""excecute the experiment and prints results"""
	for pair in pairList:	
		res.append([pair]) 
		firstRow += "%s-%s\t" % (pair[0], pair[1])
	print firstRow + "\n"
	###print first row in results table:
	
	
	n = minN
	while n <= maxN:
		res[0].append(n)
		printrow = "%d\t" % n
		game = model.Game(n, order = valorder) ##########values-?
			
		for i in range(len(pairList)):
		
			firstPlayer = getattr(agents, pairList[i][0])(game)
			secondPlayer = getattr(agents, pairList[i][0])(game)
			
			avgDiff = 0.0
				
			for reapet in range(repetitions):
				avgDiff += game.play(firstPlayer, secondPlayer)
				
			avgDiff = avgDiff / repetitions
			
			
			res[i].append(avgDiff)
			###print row in results table:
			printrow += "%f\t" % avgDiff
		print printrow + "\n"
		n = n * step
		if round(n) > n:
			n = int(round(n) - 1)
		else:
			n = int(round(n))	
		
		
if __name__ == '__main__':
	inputParser(sys.argv[1:])
	
	
