"""this module contain agents for sos game"""

import sys
from random import random, choice
from math import log, sqrt, exp
from model import *
from copy import copy

printSamplingStats = False
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
		if printSamplingStats:
			self.__printSamplingStats(stats, state)
		return next_move
		
	def __printSamplingStats(self, stats, state):
		"""print sampling statistics"""
		print "%s:" % self.name(),
		for move, stat in stats[state].items():
			print "%d,%d" % (self.game.values[move], stat.count),
		print

	def __simulate(self, select, state, stats,):
		"""simulate a game from a given state. return the score bonus"""

		if self.game.isFinalState(state):
			return self.game.calcScore(state)
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
	return 0.707

def selectUCB(state, stats):
	Cp = computeCp(state) # approximate upper bound
	totalcount = sum(stat.count for stat in stats[state].values())
	A = 2.0*Cp*sqrt(log(totalcount))
	def ucb(stat):
		return stat.getAvgValue()+A/sqrt(stat.count)
	return reduce(lambda a, b: ucb(a[1])>ucb(b[1]) and a or b,
			  stats[state].items())[0]

def selectUQB(state, stats):
	Cp = computeCp(state) # approximate upper bound
	totalcount = sum(stat.count for stat in stats[state].values())
	A = 2.0*Cp*sqrt(sqrt(totalcount))
	def uqb(stat):
		return stat.getAvgValue()+A/sqrt(stat.count)
	return reduce(lambda a, b: uqb(a[1])>uqb(b[1]) and a or b,
			  stats[state].items())[0]

def selectVOI(state, stats, voi):
	alpha = -1.0
	beta = -1.0
	
	for stat in stats[state].values():
		avg = stat.getAvgValue()
		if avg > alpha:
			beta = alpha
			alpha = avg
		elif alpha > avg and avg > beta:
			beta = avg

	return reduce(lambda a, b:
					  voi(a[1], alpha, beta) > voi(b[1], alpha, beta) \
					  and a or b,
				  stats[state].items())[0]

def voiHoeffding(stat, alpha, beta):

	def estimate(n, over, under):
		return over*exp(-0.5*n*under*under)/n

	avg = stat.getAvgValue()
	voi = avg > beta \
		and estimate(stat.count, 1+beta, avg-beta) \
		or estimate(stat.count, 1-alpha, alpha-avg)
	return voi

def selectHoeffding(state, stats):
	return selectVOI(state, stats, voiHoeffding)

# Hoeffding with Eyal's correction
def bisection(f, a, b, eps):
	"solving non-linear equation f(x)=0 by bisection"
	fa, fb = f(a), f(b)
	while True:
		if (fa>=0.0)==(fb>=0.0):
			return a
		c = 0.5*(a+b)
		if abs(a-b) <= eps:
			return c
		fc = f(c)
		if (fb>=0)==(fc>=0):
			b, fb = c, fc
		else:
			a, fa = c, fc
		
def voiEyal(stat, alpha, beta):
	def estimate(n, over, under):
		def destim(between):
			return 4.0*n*over*between*exp(-0.5*n*between*between) \
				- exp(-0.5*n*under*under)
		between = bisection(destim, under, under+over, 0.001)
	   	return ((between-under)*exp(-0.5*n*under*under) \
					+ over*exp(-0.5*n*between*between))/n

	avg = stat.getAvgValue()
	return avg > beta \
		and estimate(stat.count, 1+beta, avg-beta) \
		or estimate(stat.count, 1-alpha, alpha-avg)

def selectEyal(state, stats):
	return selectVOI(state, stats, voiEyal)

class UCT(MCTS):
	"just plain UCT"
	def __init__(self, game, samples):
		MCTS.__init__(self, game, samples, selectUCB)

class GCT(MCTS):
	"0.5-greedy then UCT"
	def __init__(self, game, samples):
		MCTS.__init__(self, game, samples, selectGreedy, selectUCB)

class QCT(MCTS):
	"sqrt(sqrt) then UCT"
	def __init__(self, game, samples):
		MCTS.__init__(self, game, samples, selectUQB, selectUCB)

class HCT(MCTS):
	"Hoeffding VOI then UCT"
	def __init__(self, game, samples):
		MCTS.__init__(self, game, samples, selectHoeffding, selectUCB)

class HRT(MCTS):
	"Hoeffding VOI then Random"
	def __init__(self, game, samples):
		MCTS.__init__(self, game, samples, selectHoeffding, selectRandom)

class ECT(MCTS):
	"Hoeffding VOI with Eyal's correction, then UCT"
	def __init__(self, game, samples):
		MCTS.__init__(self, game, samples, selectEyal, selectUCB)

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
