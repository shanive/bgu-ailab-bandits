"""simulation of games for testing"""

### 
import getopt
import sys
import model
import agents
from math import sqrt

class Conf:
	"""configuration of tournament"""
	RANDOM = 0
	ASCENDING = 1
	DESCENDING = 2
	def __init__(self):
		self.number_of_switches = 10
		self.switch_order = Conf.RANDOM
		self.repetitions = 1000
		self.firstPlayer = agents.Random
		self.secondPlayer = agents.Random
		self.score_bonus = False
		self.samples_per_state = 1000
		self.switches_values = None
		
	def __str__(self):
		"""return string for print"""
		
		return "number of switches: %d\n" % self.number_of_switches + \
			"switches order %d\n" % self.switch_order +\
			"repetitions: %d\n" % self.repetitions +\
			"players: %s %s\n" % (self.firstPlayer.__name__, self.secondPlayer.__name__) +\
			"score bonus: %s\n" % str(self.score_bonus) +\
			"samples per state: %s\n" % self.samples_per_state +\
			"switches values: %s\n" % str(self.switches_values) 


def usage():
	"""prints usage message in case of missing arguments"""
	print "Usage: python play.py --order 0/1/2 --values <list-values> --scorebonus n repetitions samples player1 player2"
	
	
def parseCommandLine(argList):
	"""receive size, players' names and repetitions number as input and begin the play"""
	agents.computeCp = agents.computeCpWinLoss #default value
	
	conf = Conf()
	
	try:
		opts, args = getopt.getopt(argList, "", ["order=", "values=", "scorebonus"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
		
	for opt,arg in opts:
		if opt == '--order' and arg in (0,1,2):
			conf.switch_order = arg
		elif opt == '--values':
			conf.switches_values = list(arg)
		elif opt == '--scorebonus':
			conf.score_bonus = True
			agents.computeCp = agents.computeCpScoreBonus
		else:
			print "Unvalid Option\n"
			usage()
			sys.exit(2) 
			
	conf.number_of_switches = int(args[0])
	conf.repetitions = int(args[1])
	conf.samples_per_state = float(args[2])
		
	conf.firstPlayer = getattr(agents, args[3])
	conf.firstPlayer = getattr(agents, args[4])
	
	return conf
		

	
def simulateGame(conf):
	"""excecute a given game between two given player for a given num of times
	
	return average difference""" 
	
	diff = 0.0
	for i in range(conf.repetitions):
		print "New Game"
		game = model.Game(conf.number_of_switches,
					values = conf.switches_values,
                                	order  = conf.switch_order, 
					scorebonus = conf.score_bonus)
		firstPlayer = conf.firstPlayer(game, conf.samples_per_state)
		secondPlayer = conf.secondPlayer(game, conf.samples_per_state)
		diff += game.play(firstPlayer, secondPlayer)
	avgDiff = diff/conf.repetitions
	print "The average difference is: %f" % avgDiff
	return avgDiff


if __name__ == '__main__':
	agents.printSamplingStats = True
	conf = parseCommandLine(sys.argv[1:])
	print >> sys.stderr, conf 
	simulateGame(conf)