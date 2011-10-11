#!usr/bin/python
"""this module contain an experiment on sos game"""

import sys
import model
import getopt
import agents
from random import choice
from optparse import OptionParser

class Conf:
	"""configuration of tournament"""
	RANDOM = 0
	ASCENDING = 1
	DESCENDING = 2
	def __init__(self, options, agentsList):
		self.number_of_switches = options.size
		self.min_samples_per_action = options.min
		self.max_samples_per_action = options.max
		self.sample_step = options.step
		if options.order in (self.RANDOM, self.ASCENDING, self.DESCENDING):
			 self.switch_order = options.order
		else:
			 self.switch_order = self.RANDOM
		self.repetitions = options.repeat
		self.agents = agentsList or [agents.Random, agents.Random]
		self.score_bonus = options.scorebonus
		self.cp = options.Cp
		self.profile = options.profile
		
	def __str__(self):
		"""return string for print"""
		agents = ""
		for agent in self.agents:
			agents += agent.name() +" "
		return "number of switches: %d\n" % self.number_of_switches + \
			"min samples per action: %d\n" % self.min_samples_per_action +\
			"max samples per action: %d\n" % self.max_samples_per_action  +\
			"sample step: %d\n" % self.sample_step +\
			"switches order %d\n" % self.switch_order +\
			"repetitions: %d\n" % self.repetitions +\
			"agents: %s\n" % agents +\
			"score bonus: %s\n" % self.score_bonus +\
			"cp: %s\n" % self.cp +\
			"profile: %s\n" % str(self.profile)
			


def nameToAgent(name):
	"""receive agent's name and return referrence to the corresponding agent's class"""
	return getattr(agents, name)

    
def parseCommandLine(argList):
    """receive input for SOS Game experiment"""

    usage = "usage: %prog [options] player-name [player-name] ..."

    parser = OptionParser(usage = usage)
    parser.add_option("--size", type = "int", dest = "size", default = 10, help = "number of switches [default: %default]")
    parser.add_option("--min", type = "int", dest = "min", default = 10, help = "min samples per action [default: %default]")
    parser.add_option("--max", type = "int", dest = "max", default = 1000, help = "max samples per action [default: %default]")
    parser.add_option("--step", type = "float", dest = "step", default = 2.0, help = "sample step [default: %default]")
    parser.add_option("--repeat", type = "int", dest = "repeat", default = 1000, help = "repetitions of each game [default: %default]")
    parser.add_option("--order", type = "int", dest = "order", default = 0, help = "switches' values order [default: %default]") ##### todo
    parser.add_option("--scorebonus", action = "store_true", dest = "scorebonus", default = False, help = "players' reward [default: %default]" )
    parser.add_option("--Cp", type = "float", dest = "Cp", help = "cp value in UCT function" )
    parser.add_option("--profile", action = "store_true", dest = "profile", default = False, help = "print profile [default: %default]")
    
    (options, args) = parser.parse_args()

    if options.Cp:
	    agents.computeCp = lambda state: option.Cp
    elif options.scorebonus:
	    agents.computeCp = agents.computeCpScoreBonus
    else:
	    agents.computeCp = agents.computeCpWinLoss
    if not args:
	    agentsList = [nameToAgent(name) for name in args]
    else:
	    agentsList = []
	     
    return Conf(options, agentsList)
   

def simulation(conf, samples):
	"""simulate a tournament for the given number of samples.
        return results"""
        results = [0.0 for a in conf.agents]
	for i in range(len(conf.agents)):
		for j in range(len(conf.agents)):
			if i!=j:
                                avgDiff = 0.0
                                for repeat in range(conf.repetitions):
                                        game = model.Game(conf.number_of_switches,
                                                             order  = conf.switch_order,
                                                             scorebonus = conf.score_bonus)
                                        avgDiff+= game.play(conf.agents[i](game, samples),
                                                            conf.agents[j](game, samples))
                                avgDiff/= conf.repetitions

				## update results
				results[i]+= avgDiff
				results[j]-= avgDiff
        return results
        
def runTournament(conf):
    """excecute the tournament and print results. """
 
    ##print the header
    print "%-10s" % "samples",
    for agent in conf.agents: print "%-10s" % agent.name(),
    print   
    
    samples = conf.min_samples_per_action
    while samples <= conf.max_samples_per_action:
        results = simulation(conf, int(round(samples)))

        ##print next line of results
        print "%-10d" % samples,
	for result in results: print "%-10f" % result,
	print

        samples *= conf.sample_step  

def profileTournament(conf):        
        """run the tournament with profiling"""
        cProfile.run('runTournament(conf)','profile')
        profile = pstats.Stats('profile')
        profile.sort_stats('time').print_stats(0.5)
       
if __name__ == '__main__':
	conf = parseCommandLine(sys.argv[1:])
	
	print >> sys.stderr, conf 
	
	# profiling commented out temporarily, please implement
    # with command line option
	if conf.profile:
                profileTournament(conf)
	else:
		runTournament(conf)

    
