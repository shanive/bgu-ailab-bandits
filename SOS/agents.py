"""this module contain agents for sos game"""

import sys
from random import choice
from model import *
from copy import copy

class Random(Agent):
	"""random algorithm for playing sos game."""
	
	def __init__(self, game, samples):
		Agent.__init__(self, game)
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		return choice(state.availableMoves())
 
class Left(Agent):
	"""algorithm for playing sos game. always choose the leftmost available move"""
	
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


class MoveStat:
        """Move statistics"""
        def __init__(self, valuesum=0.0, count=0):
                """initialize move statistics to unsampled state"""
                self.valuesum = valuesum
                self.count = count

        def updateValue(self, value):
                """receive the value of the move on a simulation and update the overall value"""
                self.valuesum += value
                self.count += 1

        def getAvgValue(self):
                """return the average value of this move"""
                return self.valuesum / self.count

def test_MoveStat():
        move = MoveStat()
        move.updateValue(0.5)
        move.updateValue(0.3)
        assert move.getAvgValue() == 0.4

class Stats(dict):
        "dictionary for node statistics"
        def __getitem__(self, state):
                "like a[b], but if b not in a, initialize to empty statistics"
                stateid = state.id()
                if stateid not in self:
                        self[stateid] = dict((move, MoveStat()) for move in state.availableMoves())
                return dict.__getitem__(self, stateid)

def select_all_then_this(state, stats, select_this):
        """select an unvisited action if any,
        then according to select_this"""
        for move, stat in stats[state].items():
                if not stat.count:
                        return move
        return select_this(state, stats)

class MCTS(Agent):
        """uniform MCTS player"""

        def __init__(self, game, samples, select_first, select_next=None):
                Agent.__init__(self, game)
                self.samples = samples
                self.select_first = lambda state, stats: \
                    select_all_then_this(state, stats, select_first)
                self.select_next = lambda state, stats: \
                    select_all_then_this(state, stats, select_next or select_first)

        def selectMove(self, state):
                """receive the state of the game and return the next move"""
                stats = Stats()
                totalsamples = self.samples*len(state.availableMoves())
                while totalsamples:
                        value = self.__simulate(self.select_first, copy(state), stats)
                        totalsamples-= 1
                return self.__bestMove(stats[state])

        def __simulate(self, select, state, stats):
                """simulate a game from a given state. return the score bonus"""

                if self.game.isFinalState(state):
                        return self.game.scoreBonus(state)
                else:
                        move = select(state, stats)
                        stat = stats[state][move]
                        isWhite = state.isWhiteTurn()
                        if isWhite:
                                state.whiteMove(move)
                        else:
                                state.blackMove(move)
                        bonus = self.__simulate(self.select_next, state, stats)
                        if isWhite:
                                stat.updateValue(bonus) # white, max
                        else:
                                stat.updateValue(-bonus) # black, min
                        return bonus

        @staticmethod
        def __bestMove(movestats):
                """receive list of Move objects and return the index of the move
                with the best average value"""
                return reduce(lambda a, b: a[1].getAvgValue()>b[1].getAvgValue() and a or b,
                              movestats.items())[0]

class Uniform(MCTS):
        "Uniform Monte Carlo sampling"
        def __init__(self, game, samples):
                MCTS.__init__(self, game, samples,
                              lambda state, stats: choice(state.availableMoves()))

def test_bestMove():
       assert 1==MCTS._MCTS__bestMove(dict([(0, MoveStat(3, 3)), (1, MoveStat(2, 1))]))

def test():
        test_MoveStat()
        test_bestMove()

test()
        
