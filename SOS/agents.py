"""this module contain agents for sos game"""

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

class MCTS(Agent):
        """uniform MCTS player"""

        def __init__(self, game, samples, select_first, select_next):
                Agent.__init__(self, game)
                self.samples = samples
                self.select_first = select_first
                self.select_next = select_next

        def selectMove(self, state):
                """receive the state of the game and return the next move"""
                moves = state.availableMoves()
                totalsamples = self.samples*len(moves)
                movestats = dict((move, MoveStat()) for move in moves)

                ## first simulate one game for each available move
                for move, stat in movestats.items():
                        nextState = self.__nextState(state, move)
                        value = self.__simulate(nextState, self.select_next)
                        stat.updateValue(value)
                        totalsamples-= 1

                ## next simulate for uniformly choosen moves
                while totalsamples:
                        move = self.select_first(state)
                        stat = movestats[move]
                        nextState = self.__nextState(state, move)
                        value = self.__simulate(nextState, self.select_next)
                        stat.updateValue(value)
                        totalsamples-= 1

                return self.__bestMove(movestats)
                        
        def __nextState(self, state, move):
                """receive a state and first move and return the next state.
                state not changed"""
                newState = copy(state)
                if newState.isWhiteTurn():
                        newState.whiteMove(move)
                else:
                        newState.blackMove(move)
                return newState

        def __simulate(self, state, select):
                """simulate a game from a given state. return the score bonus"""
                
                if self.game.isFinalState(state):
                        return self.game.scoreBonus(state)
                else:
                        move = self.select_next(state)
                        if state.isWhiteTurn():
                                state.whiteMove(move)
                        else:
                                state.blackMove(move)
                        bonus = self.__simulate(state, select)
                        # update stats for move
                        return bonus

        @staticmethod
        def __bestMove(movestats):
                """receive list of Move objects and return the index of the move
                with the best average value"""
                return reduce(lambda a, b: a[1].getAvgValue()>b[1].getAvgValue() and a or b,
                              movestats.items())[0]

class Uniform(MCTS):
        def __init__(self, game, samples):
                def select_uniform(state):
                        return choice(state.availableMoves())
                MCTS.__init__(self, game, samples, select_uniform, select_uniform)

def test_bestMove():
       assert 1==MCTS._MCTS__bestMove(dict([(0, MoveStat(3, 3)), (1, MoveStat(2, 1))]))

def test():
        test_MoveStat()
        test_bestMove()


test()
        
