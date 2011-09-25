"""this module contain agents for sos game"""

from random import choice
from model import *
from copy import copy

class Random(Agent):
	"""random algorithm for playing sos game."""
	
	def __init__(self, game):
		Agent.__init__(self, game)
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		return choice(state.availableMoves())
 
class Left(Agent):
	"""algorithm for playing sos game. always choose the leftmost available move"""
	
	def __init__(self, game):
		Agent.__init__(self, game)
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		return state.availableMoves()[0]

class Right(Agent):
	"""algorithm for playing sos game. always choose the rightmost available move"""
	
	def __init__(self, game):
		Agent.__init__(self, game)
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		moves = state.availableMoves()
		return moves[len(moves) - 1]


class Move:
        "A move in a simulated sos game"
        def __init__(self, number):
                """receive the move's number and initialize a new move"""
                self.number = number
                self.valuesum = 0.0
                self.count = 0

        def updateValue(self, value):
                """receive the value of the move on a simulation and update the overall value"""
                self.valuesum += value
                self.count += 1

        def getAvgValue(self):
                """return the average value of this move"""
                return self.valuesum / self.count

def __testMove():
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
                availables = state.availableMoves()
                moves = [Move(move) for move in availables]

                """first simulate one game for each available move"""
                for move in moves:
                        nextState = self.__nextState(state, move.number)
                        value = self.__simulate(nextState)
                        move.updateValue(value)

                repeat = self.samples * (len(moves)-1) 
                """next simulate for uniformly choosen moves"""
                for i in range(repeat):
                        move = choice(moves)
                        nextState = self.__nextState(state, move.number)
                        value = self.__simulate(nextState)
                        move.updateValue(value)

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

        def __bestMove(self, moves):
                """receive list of Move objects and return the number of the move with the best average value"""
                values = [move.getAvgValue() for move in moves]
                index = values.index(max(values))
                return moves[index].number

def test():
        __testMove()

test()
        
