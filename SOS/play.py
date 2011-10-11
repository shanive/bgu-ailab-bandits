"""simulation of games for testing"""

### 
import getopt
import sys
import model
import agents
from math import sqrt
from tournament import nameToAgent
from optparse import OptionParser

class Conf:
	"""configuration of tournament"""
	RANDOM = 0
	ASCENDING = 1
	DESCENDING = 2
	def __init__(self, options, player1, player2):
		self.number_of_switches = options.size
		if options.order in (self.RANDOM, self.ASCENDING, self.DESCENDING):
			 self.switch_order = options.order
		else:
			 self.switch_order = self.RANDOM
		self.repetitions = options.repeat
		self.firstPlayer = player1
		self.secondPlayer = player2
		self.score_bonus = options.scorebonus
		self.samples_per_state = options.sample
		#self.switches_values = None
		self.cp = options.Cp
		self.profile = options.profile
		
	def __str__(self):
		"""return string for print"""
		
		return "number of switches: %d\n" % self.number_of_switches + \
			"switches order %d\n" % self.switch_order +\
			"repetitions: %d\n" % self.repetitions +\
			"players: %s %s\n" % (self.firstPlayer.__name__, self.secondPlayer.__name__) +\
			"score bonus: %s\n" % str(self.score_bonus) +\
			"samples per state: %s\n" % self.samples_per_state +\
			"cp: %s\n" % str(self.cp) +\
			"profile: %s\n" % str(self.profile)
			
	
	
def parseCommandLine(argList):
	"""receive size, players' names and repetitions number as input and begin the play"""
	
	usage = "usage: %prog [options] player-name player-name"

    	parser = OptionParser(usage = usage)
	parser.add_option("--samples", type = "int", dest = "sample", default = 1000, help = "number of samples per action [default: %default]")
	parser.add_option("--size", type = "int", dest = "size", default = 10, help = "number of switches [default: %default]")
    	parser.add_option("--repeat", type = "int", dest = "repeat", default = 1000, help = "repetitions of each game [default: %default]")
  	parser.add_option("--order", type = "int", dest = "order", default = 0, help = "order of switches' value [default: %default]")
   	parser.add_option("--scorebonus", action = "store_true", dest = "scorebonus", default = False, help = "players' reward [default: %default]" )
   	parser.add_option("--Cp", type = "float", dest = "Cp", help = "cp value in UCT function" )
   	parser.add_option("--profile", action = "store_true", dest = "profile", default = False, help = "print profile [default: %default]")
    
    	(options, args) = parser.parse_args()
	
	if options.Cp:
	    agents.computeCp = lambda state: options.Cp
   	elif options.scorebonus:
	    agents.computeCp = agents.computeCpScoreBonus
    	else:
	    agents.computeCp = agents.computeCpWinLoss
	
	return Conf(options, nameToAgent(args[0]), nameToAgent(args[1]))

	
	
	
	
	
	
	
	#agents.computeCp = agents.computeCpWinLoss #default value
	
	#conf = Conf()
	
	#try:
		#opts, args = getopt.getopt(argList, "", ["order=", "values=", "scorebonus"])
	#except getopt.GetoptError:
		#usage()
		#sys.exit(2)
		
	#for opt,arg in opts:
		#if opt == '--order' and arg in (0,1,2):
			#conf.switch_order = arg
		#elif opt == '--values':
			#conf.switches_values = list(arg)
		#elif opt == '--scorebonus':
			#conf.score_bonus = True
			#agents.computeCp = agents.computeCpScoreBonus
		#else:
			#print "Unvalid Option\n"
			#usage()
			#sys.exit(2) 
			
	#conf.number_of_switches = int(args[0])
	#conf.repetitions = int(args[1])
	#conf.samples_per_state = float(args[2])
		
	#conf.firstPlayer = getattr(agents, args[3])
	#conf.firstPlayer = getattr(agents, args[4])
	
	#return conf
		

	
def simulateGame(conf):
	"""excecute a given game between two given player for a given num of times
	
	return average difference""" 
	
	diff = 0.0
	for i in range(conf.repetitions):
		print "New Game"
		game = model.Game(conf.number_of_switches,
                                	order  = conf.switch_order, 
					scorebonus = conf.score_bonus)
		firstPlayer = conf.firstPlayer(game, conf.samples_per_state)
		secondPlayer = conf.secondPlayer(game, conf.samples_per_state)
		diff += game.play(firstPlayer, secondPlayer)
	avgDiff = diff/conf.repetitions
	print "The average difference is: %f" % avgDiff
	return avgDiff
	
	
def playProfile(conf):        
        """run the tournament with profiling"""
        cProfile.run('simulateGame(conf)','playprofile')
        profile = pstats.Stats('playprofile')
        profile.sort_stats('time').print_stats(0.5)


if __name__ == '__main__':
	agents.printSamplingStats = True
	conf = parseCommandLine(sys.argv[1:])
	print >> sys.stderr, conf 
	if conf.profile:
                playProfile(conf)
	else:
		simulateGame(conf)
	