"""this module contain agents for sos game

methods:
	randomPlayer(moves) -- choose the next move randomly
	leftPlayer(moves) -- always choose the leftmost move
"""

from random import choice
from model import Agent
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


class Uniform(Agent):
	"""uniform MCTS player"""	
	
	def __init__(self, game, samples):
		Agent.__init__(self, game)
		self.samples = samples
		
	def selectMove(self, state):
		"""receive the state of the game and return the next move"""
		moves = state.availableMoves()
		moveValues = [0.0 for move in moves]
		### first sample each move:
		copystate = state.copy(state)
		for i in range(len(moves)):
			simulate