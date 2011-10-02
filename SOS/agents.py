"""this module contain agents for sos game"""

import sys
from random import random, choice
from math import log, sqrt
from model import *
from copy import copy

computeCp = None

class Random(Agent):
	"""random algorithm for playing sos game."""
	
	def __init__(self, game, samples):
		Agent.__init__(self, game)
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		return choice(state.availableMoves())
 
class Left(Agent):
	"""algorithm for playing sos game. 
	always choose the leftmost available move"""
	
	def __init__(self, game, samples):
		Agent.__init__(self, game)
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		return state.availableMoves()[0]

class Right(Agent):
	"""algorithm for playing sos game. always choose the rightmost available move"""
	
	def __init__(self, game, samples):
		Agent.__init__(self, game)
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		moves = state.availableMoves()
		return moves[len(moves) - 1]


def selectAllThenThis(state, stats, selectThis):
        """select an unvisited action if any,
        then according to select_this"""
        for move, stat in stats[state].items():
                if not stat.count:
                        return move
        return selectThis(state, stats)

def bestMove(state, stats):
        """receive list of Move objects and return the index of the move
        with the best average value"""
        return reduce(lambda a, b: a[1].getAvgValue()>b[1].getAvgValue() and a or b,
                      stats[state].items())[0]
		   
class MCTS(Agent):
        """uniform MCTS player"""

        def __init__(self, game, samples, selectFirst, selectNext=None):
                Agent.__init__(self, game)
                self.samples = samples
                self.selectFirst = lambda state, stats: \
                    selectAllThenThis(state, stats, selectFirst)
                self.selectNext = lambda state, stats: \
                    selectAllThenThis(state, stats, selectNext or selectFirst)

        def selectMove(self, state):
                """receive the state of the game and return two values: 
		one is the next move and the other is the state's statistics: (statistics, next move)"""
                stats = Stats()
                totalsamples = self.samples*len(state.availableMoves())
                while totalsamples:
                        value = self.__simulate(self.selectFirst, copy(state), stats)
                        totalsamples-= 1
		next_move = bestMove(state, stats)
                return (next_move, stats)

        def __simulate(self, select, state, stats,):
                """simulate a game from a given state. return the score bonus"""

                if self.game.isFinalState(state):
			return self.game.calcScore(state)
                        #return self.game.scoreBonus(state)
                else:
                        move = select(state, stats)
                        stat = stats[state][move]
                        isWhite = state.isWhiteTurn()
                        if isWhite:
                                state.whiteMove(move)
                        else:
                                state.blackMove(move)
                        bonus = self.__simulate(self.selectNext, state, stats)
                        if isWhite:
                                stat.updateValue(bonus) # white, max
                        else:
                                stat.updateValue(-bonus) # black, min
                        return bonus

### uniform random selector

def selectRandom(state, stats):
	"""select one of available moves randomly,
	with equal probability"""
	return choice(state.availableMoves())

class Uniform(MCTS):
        "Uniform Monte Carlo sampling"
        def __init__(self, game, samples):
                MCTS.__init__(self, game, samples, selectRandom)

### adaptive selectors

## 0.5-greedy

def selectGreedy(state, stats):
        """select best move with probability 0.5,
        or another move with uniform probability"""
        moves = state.availableMoves()
        if len(moves)==1 or random() > 0.5 * len(moves)/(len(moves)-1):
                return bestMove(state, stats)
        else:
                return choice(moves)

## UCB

def computeCpScoreBonus(state):
	"""compute Cp if using score bonus"""
	return 0.5*state.size*len(state.availableMoves())
 
def computeCpWinLoss(state):
	"""compute Cp without score bonus"""
	return 1.0

def selectUCB(state, stats):
	# 1, -1 => Cp = 1
	# 1, 0  => Cp = 0.5
        Cp = computeCp(state) # approximate upper bound
        totalcount = sum(stat.count for stat in stats[state].values())
        A = 2.0*Cp*sqrt(log(totalcount))
        def ucb(stat):
                return stat.getAvgValue()+A/sqrt(stat.count)
        return reduce(lambda a, b: ucb(a[1])>ucb(b[1]) and a or b,
                      stats[state].items())[0]

class UCT(MCTS):
        def __init__(self, game, samples):
                MCTS.__init__(self, game, samples, selectUCB)

class GCT(MCTS):
        def __init__(self, game, samples):
                MCTS.__init__(self, game, samples, selectGreedy, selectUCB)

class GRT(MCTS):
        def __init__(self, game, samples):
                MCTS.__init__(self, game, samples, selectGreedy, selectRandom)


### Tests

def test_bestMove():
       assert 1==bestMove(0, {0: dict([(0, MoveStat(3, 3)), (1, MoveStat(2, 1))])})

def test():
        test_MoveStat()
        test_bestMove()

test()
        
