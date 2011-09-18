 #!/usr/bin/python
 #argecho.py
import sys
import sosGame
import getopt
from random import choice

def usage():
	print "Usage: python sosTest.py --min <min-n> --max <max-n> --step <step-n> --repeat <reapetions> -u/-d"  
 
def randomPlayer(moves):
	"""random algorithm for playing sos game.
	receives the available moves.
	return the move to choose"""

	return choice(moves)
 
def leftPlayer(moves):
	"""random algorithm for playing sos game.
	receives the available moves.
	return the move to choose"""
	return moves[0]
 
 
def inputParser(argList):
	"""receive input for SOS Game experiment"""
	### default values:
	minN = 10
	maxN = 1000
	step = 2
	repetitions = 100000
	order = 'r' #'r' = random, 'u' = up (min to max), 'd' = down (max to min)  
	
	try:
		opts, args = getopt.getopt(argList,"ud",["min=","max=","step=", "repeat="])
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
		elif opt == '-u':
			order = 'u'
		elif opt == '-d':
			order = 'd'
		else:
			print "Unvalid Option\n"
			usage()
			sys.exit(2)  
			
 	sosExperiment(minN, maxN, step, repetitions, order)
 		
def sosExperiment(minN, maxN, step, repetitions, order):
	
	res = [["n"],["difference"]]
	game = sosGame.SOSGame(randomPlayer, leftPlayer, minN, order)
	n = minN
	while n <= maxN:
		game.changeSize(n, order)
		avgDiff = 0.0	
		for reapet in range(repetitions):
			avgDiff += game.newGame()
		avgDiff = avgDiff / repetitions
		
		res[0].append(n)
		res[1].append(avgDiff)
		
		n = n * step
		if round(n) > n:
			n = int(round(n) - 1)
		else:
			n = int(round(n))	
		
	printResults(res)
	
def printResults(results):
	
	strToPrint = ""
	strToPrint = "%-10s %-10s\n" % (results[0][0], results[1][0])
	for row in range(1, len(results[0])):
		strToPrint += "%-10d %-10f\n" % (results[0][row], results[1][row])
	print strToPrint
		
if __name__ == '__main__':
	inputParser(sys.argv[1:])
	
	
