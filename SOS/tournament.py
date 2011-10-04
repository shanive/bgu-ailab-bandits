#!usr/bin/python
"""this module contain an experiment on sos game"""

import sys
import model
import getopt
import agents
from random import choice
import cProfile



class Conf:
	"""configuration of tournament"""
	RANDOM = 0
	ASCENDING = 1
	DESCENDING = 2
	def __init__(self):
		self.number_of_switches = 10
		self.min_samples_per_action = 10
		self.max_samples_per_action = 1000
		self.sample_step = 2.0
		self.switch_order = Conf.RANDOM
		self.repetitions = 1000
		self.agents = [agents.Random, agents.Random]
		self.score_bonus = False
		self.cp = 0.0
		self.profile = False
		
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
			"cp: %f\n" % self.cp +\
			"profile output file: %s\n" % str(self.profile)
			


def nameToAgent(name):
	"""receive agent's name and return referrence to the corresponding agent's class"""
	return getattr(agents, name)


def usage():
    """print usage message to standart output"""
    print "Usage: python tournament.py --cp <cp-value> --size switches --min min-samples --max max-samples --step sample-step --repeat repetitions --order 0/1/2 --scorebonus --profile player-name [player-name]..."
    
def parseCommandLine(argList):
    """receive input for SOS Game experiment"""
    ### default values:
    agents.computeCp = agents.computeCpWinLoss
    
    conf = Conf()
    
    try:
        opts, args = getopt.getopt(argList,"",["min=","max=","step=", "repeat=", "order=",\
						"size=", "scorebonus", "Cp=", "profile"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt,arg in opts:
	if opt == '--size':
		conf.number_of_switches = int(arg)
        elif opt == '--min':
            conf.min_samples_per_action = float(arg)
        elif opt == '--max':
            conf.max_samples_per_action = float(arg)
        elif opt == '--step':
            conf.sample_step = float(arg)
        elif opt == '--repeat':
            conf.repetitions = int(arg)
        elif opt == '--order' and int(arg) in (conf.RANDOM, conf.ASCENDING, conf.DESCENDING):
            conf.switch_order = int(arg)
	elif opt == '--scorebonus':
	    conf.score_bonus = True
	    agents.computeCp = agents.computeCpScoreBonus
	elif opt == '--Cp':
	    conf.cp = float(arg)
	    agents.computeCp = lambda state: conf.cp 
	elif opt == '--profile':
	    conf.profile = True
        else:
            print "Unvalid Option\n"
            usage()
            sys.exit(2)
       
	    
    if args:
	    conf.agents = [nameToAgent(name) for name in args]
	                
    return conf

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
        
        
if __name__ == '__main__':
	conf = parseCommandLine(sys.argv[1:])
	
	print >> sys.stderr, conf 
	
	# profiling commented out temporarily, please implement
    # with command line option
	if conf.profile:
		cProfile.run('runTournament(conf)')
	else:
		runTournament(conf)

    
