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


class Move:
        "A move in a simulated sos game"
        def __init__(self, index, valuesum=0.0, count=0):
                """receive the move's index and initialize a new move"""
                self.index = index
                self.valuesum = valuesum
                self.count = count

        def updateValue(self, value):
                """receive the value of the move on a simulation and update the overall value"""
                self.valuesum += value
                self.count += 1

        def getAvgValue(self):
                """return the average value of this move"""
                return self.valuesum / self.count

def test_Move():
        move = Move(3)
        move.updateValue(0.5)
        move.updateValue(0.3)
        assert move.getAvgValue() == 0.4

class Uniform(Agent):
        """uniform MCTS player"""

        def __init__(self, game, samples):
                Agent.__init__(self, game)
                self.samples = samples

        def selectMove(self, state):
                """receive the state of the game and return the next move"""
                moves = [Move(index) for index in state.availableMoves()]

                totalsamples = self.samples*len(moves)
                ## first simulate one game for each available move
                for move in moves:
                        nextState = self.__nextState(state, move.index)
                        value = self.__simulate(nextState)
                        move.updateValue(value)
                        totalsamples-= 1

                ## next simulate for uniformly choosen moves
                while totalsamples:
                        move = choice(moves)
                        nextState = self.__nextState(state, move.index)
                        value = self.__simulate(nextState)
                        move.updateValue(value)
                        totalsamples-= 1

                return self.__bestMove(moves)
                        
        def __nextState(self, state, move):
                """receive a state and first move and return the next state.

                state not changed"""
                newState = copy(state)
                if newState.isWhiteTurn():
                        newState.whiteMove(move)
                else:
                        newState.blackMove(move)
                return newState

        def __simulate(self, state):
                """simulate a game from a given state. return the score bonus"""
                
                while not self.game.isFinalState(state):
                        move = choice(state.availableMoves())
                        if state.isWhiteTurn():
                                state.whiteMove(move)
                        else:
                                state.blackMove(move)
                return self.game.scoreBonus(state)

        @staticmethod
        def __bestMove(moves):
                """receive list of Move objects and return the index of the move
                with the best average value"""
                return reduce(lambda a, b: a.getAvgValue()>b.getAvgValue() and a or b,
                              moves).index

def test_bestMove():
       assert 1==Uniform._Uniform__bestMove([Move(0, 3, 3), Move(1, 2, 1)])

def test():
        test_Move()
        test_bestMove()


test()
        
