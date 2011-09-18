from random import choice
from random import shuffle

class State:
	GRAY = 0
	WHITE = 1
	BLACK = -1
	
	def __init__(self, n):
		self.colors = [State.GRAY] * n
	
	def __someMoves(self, color):
		return [i for i in range(len(self.colors)) if self.colors[i]==color]
	
	def availableMoves(self): return self.__someMoves(State.GRAY)
	
	def __move(self, i, color):
		assert self.colors[i]==State.GRAY
		self.colors[i] = color

	def whiteMove(self, i): self.__move(i, State.WHITE)
	def blackMove(self, i): self.__move(i, State.BLACK)
		
	def isFinalState(self):
		return not self.availableMoves()
	
	def whites(self): return self.__someMoves(State.WHITE)
	def blacks(self): return self.__someMoves(State.BLACK)

class Game:
	def __init__(self, n, values = None, order = 'r'):
		self.n = n
		self.values = values or self.__initValues(order)
		
	def __initValues(self, order):
		values = range(self.n)
		if order == 'd':
			values.reverse()  
		elif order == 'r':	
			shuffle(values)
		#else order == 'u'
		return values
	
	def initialState(self):
		return State(self.n)
	
	def scoreBonus(self, state):
		return sum(self.values[i] for i in state.whites()) \
		       - sum(self.values[i] for i in state.blacks())


def test_game():
	game = Game(4, [3, 2, 0, 1])
	state = game.initialState()
	state.whiteMove(2)
	state.blackMove(0)
	state.whiteMove(1)
	state.blackMove(3)
	assert game.scoreBonus(state) == -2
	
#class Move:
	#"""Simulation of a move in SOS game.
	#Every move has value and color.
	#A move's color represents the move's state: gray = available, white = choosen by white player, black = choosen by black player"""
	#def __init__(self, value, color):
		#self.__value  = value
		#self.__color = color
		
	#def setValue(self, value):
		#"""changes the move's value"""
		#self.__value = value 
	
	#def setColor(self, color):
		#"""changes the move's color"""
		#self.__color = color
		
	#def getValue(self):
		#return self.__value
	
	#def getColor(self):
		#return self.__color
		
#class SOS:
	#"Implementation of Sum Of Switches Game"
	
	#def __init__(self, n):
		#"""Initialize SOS game,
		#receives the number of possible moves (even number)""" 
		#self.__n = n
		
				## initial values for moves
		
		
	#def getn(self):
		#"""returns the number of moves"""
		#return self.__n
	
	#def restartGame(self):
		#"""start a game with the same moves' values"""
		#for move in self.__moves:
			#move.setColor('gray')
		
			
	#def newGame(self):
		#"""starts a new game"""
		
		#self.__moves = []
				
		#src = [i for i in range(self.__n)]	#moves' values
		
		###initialize the moves' values:
		#for i in range(self.__n):
			#value = choice(src)		#choose value randomly for move number i
			#move = Move(value, 'gray')
			#self.__moves.append(move)
			#src.remove(value)		#remove the value from values list to prevent duplicate values 
			
			
		
	#def whiteMove(self, move):
		#"""add a given move number to white player's moves"""
		#self.__moves[move].setColor('white')
		
	#def blackMove(self, move):
		#"""add a given move number to black player's moves"""
		#self.__moves[move].setColor('black')	

	
	#def endGame(self):
		#"""return the distance between the white player's score and the black player's score"""
		
		#whiteScore = 0
		#blackScore = 0
		
		#for move in self.__moves:
			#if move.getColor() == 'white':
				#whiteScore += move.getValue() 	
			#else:
				#blackScore += move.getValue()
				
		#return whiteScore - blackScore
	
	#def availableMoves(self):
		#"""returns a list of unchoosen moves"""
		#grayMoves = []
		#for i in range(self.__n):
			#if self.__moves[i].getColor() == 'gray':
				#grayMoves.append(i)
		#return grayMoves


def test_availableMoves():
	state = State(4)
	assert state.availableMoves()==[0, 1, 2, 3]

	state.whiteMove(2)
	state.blackMove(0)
	assert state.availableMoves()==[1,3]

def test_isFinalState():
	state = State(4)
	
	state.whiteMove(2)
	state.blackMove(0)
	assert not state.isFinalState()
	
	state.whiteMove(1)
	state.blackMove(3)
	assert state.isFinalState()
	
def test_whites():
	state = State(4)
	
	state.whiteMove(2)
	state.blackMove(0)
	state.whiteMove(1)
	state.blackMove(3)
	assert state.whites()==[1,2]
	
def test_blacks():
	state = State(4)
	
	state.whiteMove(2)
	state.blackMove(0)
	state.whiteMove(1)
	state.blackMove(3)
	assert state.blacks()==[0,3]
	
def test_state():
	test_availableMoves()
	test_isFinalState()
	test_whites()
	test_blacks()
	
def test():
	test_state()
	test_game()
	
test()
	