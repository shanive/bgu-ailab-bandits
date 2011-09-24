"""this module contain an experiment on sos game"""

import sys
import model
import getopt
import agents
from random import choice

def listToPairs(lst):
    """receive list of elements and return a list of pairs of the elements"""
    pairs = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if not i == j:
                pairs.append((lst[i],lst[j]))
    return pairs
    


def usage():
    """print usage message to standart output"""
    print "Usage: python tournament.py --min min-n --max max-n --step step-n --repeat reapetions --order r/a/d --samples sample-num player-name [player-name]..."
    
def inputParser(argList):
    """receive input for SOS Game experiment"""
    ### default values:
    minN = 10
    maxN = 10
    step = 2
    repetitions = 100000
    order = 'r'  #'r' = random, 'a' = ascending, 'd' = descending)  
    #white = 'random'
    #black = 'random'
    samples = 100   ##### for MCST algorithm
    
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
            
    tournament(minN, maxN, step, repetitions, order, samples, args)

def twoPlayersGame(game, repetitions, pair, samples):
    """simulate a game between to given players. return the average difference"""
    avgDiff = 0.0
    
    first = getattr(agents, pair[0])
    second = getattr(agents, pair[1])

    if pair[0] == 'Uniform':
            firstPlayer = first(game, samples)
    else:
            firstPlayer = first(game)

    if pair[1] == 'Uniform':
            secondPlayer = second(game, samples)
    else:
            secondPlayer = second(game)
    
    for reapet in range(repetitions):
        avgDiff += game.play(firstPlayer, secondPlayer)
        
    return avgDiff / repetitions
    
def simulateGame(n, valuesOrder, repeat, players, database, samples):
    """receive game details and simulate a game. update results in database"""
    game = model.Game(n, order = valuesOrder) ##########values-?
            
    for i in range(len(players)):
        avgDiff = twoPlayersGame(game, repeat, players[i], samples)         
        database[i+1].append(avgDiff)
        print "%f\t" % avgDiff,
            
    print
        
def tournament(minN, maxN, step, repeat, valorder, samples, players):
    """excecute the tournament and print results"""
    pairs = listToPairs(players)
    results = [["n"]]
    
    """print first row"""
    print "n\t",
    for player1, player2 in pairs:  
        results.append([(player1,player2)])
        print "%s-%s\t" % (player1, player2),
    print   
    n = minN
    while n <= maxN:
        results[0].append(n)
        print "%d\t" % n,
        simulateGame(n, valorder, repeat, pairs, results, samples)
        print
        n = n * step
        if round(n) > n:
            n = int(round(n) - 1)
        else:
            n = int(round(n))   
        
        
if __name__ == '__main__':
        inputParser("--min 10 --max 1000 --order a --repeat 100 Random Left Uniform".split())
    #inputParser(sys.argv[1:])
    
    
