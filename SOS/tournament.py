"""this module contain an experiment on sos game"""

import sys
import model
import getopt
import agents
from random import choice


class Conf:
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
		agents = ""
		for agent in self.agents:
			agents += agent.name() +" "
		return "number of switches: %d\n" % self.number_of_switches + \
			"min samples per action: %d\n" % self.min_samples_per_action +\
			"max samples per action: %d\n" % self.max_samples_per_action  +\
			"semple step: %d\n" % self.sample_step +\
			"switches order %d\n" % self.switch_order +\
			"repetitions: %d\n" % self.repetitions +\
			"agents: %s" % agents

#def listToPairs(lst):
    #"""receive list of elements and return a list of pairs of the elements"""
    #pairs = []
    #for i in range(len(lst)):
        #for j in range(len(lst)):
            #if not i == j:
                #pairs.append((lst[i],lst[j]))
    #return pairs
    
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

def twoPlayersGame(game, samples, firstplayer, secondPlayer, conf):
    """simulate a game between to given players. return the average difference"""
    avgDiff = 0.0
    
    for reapet in range(repetitions):
        avgDiff += game.play(firstPlayer, secondPlayer)
        
    return avgDiff / repetitions
   
    
def simulation(conf, game, samples, players, dict):
	"""receive samples num and simulate a tournament. update results in dict"""
	    
	for playerA in players):
		for playerB in players):
			if not playerA == playerB: 
				avgDiff = twoPlayersGame(game, samples, playerA, playerB, conf)
				"""update results"""
				dict[playerA.name()] += avgDiff
				dict[playerB.name()] += avgDiff * -1   #############ask
        
def tournament(conf):
    """excecute the tournament and print results. """
 
    """print first line of results"""
     #"""print first row"""
    print "samples\t",
    for agent in conf.agents:  
        print agent.name() + '\t',
    print   
    
    game  = model.Game(conf.number_of_switches, order  = conf.switch_order)
    players = [agent(game) for agent in conf.agents]
    results = dict((a.name(), 0.0) for a in conf.agents)
    
    samples = conf.min_samples_per_action
    while samples <= conf.max_samples_per_action:
        
        print "%d\t" % samples,
        simulation(conf, game, samples, players, dict)
        """print next line of results"""
	for agent in conf.agents:
		print dict[agent.name()] + '\t'
	print
	
        samples *= step
        #if round(n) > n:
            #n = int(round(n) - 1)
        #else:
            #n = int(round(n))   
        
        
if __name__ == '__main__':
	conf = parseCommandLine(sys.argv[1:])
	
	print >> sys.stderr, conf 
	
	# runTournament(conf)
	
    
