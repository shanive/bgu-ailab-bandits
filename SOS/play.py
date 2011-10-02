"""simulation of games for testing"""

### 
import getopt
import sys
import model
import agents

def usage():
	"""prints usage message in case of missing arguments"""
	print "Usage: python play.py --order r/a/d --values <list-values> n repetitions samples player1 player2"
	
	
def parse(argList):
	"""receive size, players' names and repetitions number as input and begin the play"""
	
	#default values:
	order = 'r' 
	values = None
	
	try:
		opts, args = getopt.getopt(argList, "", ["order=", "values="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
		
	for opt,arg in opts:
		if opt == '--order' and arg in ('r','a','d'):
			order = arg
		elif opt == '--values':
			values = list(arg)
		else:
			print "Unvalid Option\n"
			usage()
			sys.exit(2) 
	
	game = model.Game(int(args[0]), values, order)
	
	firstPlayer = getattr(agents, args[3])(game, int(args[2]))
	secondPlayer = getattr(agents, args[4])(game, int(args[2]))
	agents.computeCp = agents.computeCpWinLoss
	play(game, int(args[1]), firstPlayer, secondPlayer)
	
	

	
def play(game, repeat, firstPlayer, secondPlayer):
	"""excecute a given play between two given player for a given num of times
	
	return average difference""" 
	
	diff = 0.0
	for i in range(repeat):
		diff += game.play(firstPlayer, secondPlayer)
	avgDiff = diff/repeat
	print "The average difference is: %f" % avgDiff
	return avgDiff



if __name__ == '__main__':
	agents.printSamplingStats = True
	parse(sys.argv[1:])

