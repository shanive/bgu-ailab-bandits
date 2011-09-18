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
		if order == 'u':    # U)p
			pass # already in accending order
		elif order == 'd':  # D)own
			values.reverse()  
		elif order == 'r':	# R)andom
			shuffle(values)
		return values
	
	def initialState(self):
		"create an initial state of the game"
		return State(self.n)

	def __score(self, indices):
		"return total score of switches at the indices"
		return sum(self.values[i] for i in indices)
	
	def scoreBonus(self, state):
		"compute game score bonus"
		return self.__score(state.whites()) - self.__score(state.blacks())

def test_game():
	game = Game(4, [3, 2, 0, 1])
	state = game.initialState()
	state.whiteMove(2)
	state.blackMove(0)
	state.whiteMove(1)
	state.blackMove(3)
	assert game.scoreBonus(state) == -2
	
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
	
def test_whites_blacks():
	state = State(4)
	
	state.whiteMove(2)
	state.blackMove(0)
	state.whiteMove(1)
	state.blackMove(3)
	assert state.whites()==[1,2]
	assert state.blacks()==[0,3]
	
def test_state():
	test_availableMoves()
	test_isFinalState()
	test_whites_blacks()
	
def test():
	test_state()
	test_game()
	
test()
	
