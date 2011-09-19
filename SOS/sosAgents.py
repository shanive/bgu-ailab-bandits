"""this module contain agents for sos game

methods:
	randomPlayer(moves) -- choose the next move randomly
	leftPlayer(moves) -- always choose the leftmost move
"""

from random import choice
import sos
from copy import copy

def random(moves):
	"""random algorithm for playing sos game."""

	return choice(moves)
 
def left(moves):
	"""algorithm for playing sos game. always choose the leftmost move"""
	return moves[0]

def right(moves):
	"""algorithm for playing sos game. always choose the rightmost move"""
	return moves[len(moves) - 1]


def uniform(state, samples):
	"""return next move"""
	availableMoves = state.availableMoves()
	movesValues = [0.0 for move in availableMoves]
	
	for smp in range(samples):
		randMove = choice(availableMoves)
		index = availableMoves.index(randMove)
		copystate = state.copy()
		copystate.whiteMove(randMove)
		
		randMoveValue = simulation(copystate, samples, whiteTurn)
		movesValues[index] +=  randMoveValue / samples
	
	bestMoveIndex =  availableMoves.index(max(movesValues))
	return availableMoves[bestMoveIndex]
	

#def simulation(state, samples, whiteTurn, movesValues):
	#"""algorithm for playing sos game. uniform MCTS player.
	
	#receives sos game state and number of sampling"""
	
	#"""simulate an sos game from a given state"""	
	#if state.isFinalState():
		#return `bestMove(movesValues)               #####todo
	#else:
		#for smp in range(samples):
			#moves = state.availableMoves()
			#randMove = choice(moves)
			#copystate = state.copy()
			#if whiteTurn:
				#copystate.whiteMove(randMove)
			#else:
				#copystate.blackMove(randMove)
			#value = simulation(copystate, samples, not whiteTurn, )
		
		
		
	#movesValue = [0 for move in state.availableMoves()]	###values of every move according to simulations
	#simulations = len(moves)
	#for smp in range(samples):
		#randMove = choice(moves)	###choose move randomly
		#uniform(moves.remove(randMove), samples)	###simulate chosing randMove.
	
	