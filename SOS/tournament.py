"""this module contain an experiment on sos game"""

import sys
import model
import getopt
import agents
from random import choice


class Conf:
	"""configuration of tournament"""
	RANDOM = 0
	ASCENDING = 1
	DESCENDING = 2
	def __init__(self):
		self.number_of_switches = 10
		self.min_samples_per_action = 10
		self.max_samples_per_action = 1000
		self.sample_step = 2
		self.switch_order = Conf.RANDOM
		self.repetitions = 1000
		self.agents = [agents.Random, agents.Random]
		
	def __str__(self):
		"""return string for print"""
		agents = ""
		for agent in self.agents:
			agents += agent.name() +" "
		return "number of switches: %d\n" % self.number_of_switches + \
			"min samples per action: %d\n" % self.min_samples_per_action +\
			"max samples per action: %d\n" % self.max_samples_per_action  +\
			"semple step: %d\n" % self.sample_step +\
			"switches order %d\n" % self.switch_order +\
			"repetitions: %d\n" % self.repetitions +\
			"agents: %s\n" % agents


def nameToAgent(name):
	"""receive agent's name and return referrence to the corresponding agent's class"""
	return getattr(agents, name)


def usage():
    """print usage message to standart output"""
    print "Usage: python tournament.py --size switches --min min-samples --max max-samples --step sample-step --repeat reapetions --order r/a/d player-name [player-name]..."
    
def parseCommandLine(argList):
    """receive input for SOS Game experiment"""
    ### default values:
    conf = Conf()
    
    try:
        opts, args = getopt.getopt(argList,"",["min=","max=","step=", "repeat=", "order=", "size="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt,arg in opts:
	if opt == '--size':
		conf.number_of_switches = int(arg)
        elif opt == '--min':
            conf.min_samples_per_action = int(arg)
        elif opt == '--max':
            conf.max_samples_per_action = int(arg)
        elif opt == '--step':
            conf.sample_step = float(arg)
        elif opt == '--repeat':
            conf.repetitions = int(arg)
        elif opt == '--order' and int(arg) in (conf.RANDOM, conf.ASCENDING, conf.DESCENDING):
            conf.switch_order = int(arg)
        else:
            print "Unvalid Option\n"
            usage()
            sys.exit(2)
	    
    if args:
	    conf.agents = [nameToAgent(name) for name in args]
	                
    return conf

def twoPlayersGame(game, firstPlayer, secondPlayer, repetitions):
    """simulate a game between to given players. return the average difference"""
    avgDiff = 0.0
    
    for reapet in range(repetitions):
        avgDiff += game.play(firstPlayer, secondPlayer)
        
    return avgDiff / repetitions
   
    
def simulation(conf, game, samples, results):
	"""simulate a tournament for a givem game and given number of samples. update results"""
	players = [agent(game, samples) for agent in conf.agents]    
	for playerA in players:
		for playerB in players:
			if not playerA == playerB: 
				avgDiff = twoPlayersGame(game, playerA, playerB, conf.repetitions)
				##update results
				results[playerA.name()] += avgDiff
				results[playerB.name()] += avgDiff * -1   #############ask
        
def runTournament(conf):
    """excecute the tournament and print results. """
 
    ##print first line of results
    print "%-10s" % "samples",
    for agent in conf.agents:  
        print "%-10s" % agent.name(),
    print   
    
    game  = model.Game(conf.number_of_switches, order  = conf.switch_order)
    results = dict((a.name(), 0.0) for a in conf.agents)
    
    samples = conf.min_samples_per_action
    while samples <= conf.max_samples_per_action:
        
        print "%-10d" % samples,
        simulation(conf, game, samples, results)
        ##print next line of results
	for agent in conf.agents:
		print "%-10f" % (results[agent.name()] / samples),
	print
	
        samples *= conf.sample_step  
        
        
if __name__ == '__main__':
	conf = parseCommandLine(sys.argv[1:])
	
	print >> sys.stderr, conf 
	
	runTournament(conf)
	
    
