
"""This module contain the classes State and Game"""

from random import choice
from random import shuffle
from copy import copy

class State:
        
        """simulate a state of an sos game
        
        methods:
        availableMoves() -- return list of unchoosen moves
        whiteMove(i) -- choose move i to be white's move
        blackMove(i) -- choose move i to be black's move
        isFinal() -- return true if there are no available moves
        whites() -- return list of white's moves
        blacks() -- return list of black's moves
        """
        
        GRAY = 0
        WHITE = 1
        BLACK = 2
        
        def __init__(self, n=0):
                """receive the number of moves in the game"""
                self.size = n
                self.colors = [State.GRAY]*n
                self.turn = State.WHITE
                self.idmemo = None
                self.movememo = {}
                
        def __copy__(self):
                """implementation of deepcopy,
                returns a copy of the state for simulation"""
                state = State()
                state.size = self.size
                state.colors = self.colors[:]
                state.turn = self.turn
                state.idmemo = self.idmemo
                state.movememo = self.movememo
                return state

        def __someMoves(self, color):
                return [i for i in range(len(self.colors)) if self.colors[i]==color]
        
        def availableMoves(self): 
                stateid = self.id()
                if stateid not in self.movememo:
                        self.movememo[stateid] = self.__someMoves(State.GRAY)
                return self.movememo[stateid]
        
		def set_turn(self, color):
			self.turn = color

        def __move(self, i, color):
                assert self.colors[i]==State.GRAY
                self.colors[i] = color
                if self.turn==State.WHITE:
                        self.turn = State.BLACK
                else:
                        self.turn = State.WHITE
                self.idmemo = None

        def isWhiteTurn(self): return self.turn==State.WHITE

        def whiteMove(self, i): self.__move(i, State.WHITE)
        def blackMove(self, i): self.__move(i, State.BLACK)
                
        def whites(self): return self.__someMoves(State.WHITE)
        def blacks(self): return self.__someMoves(State.BLACK)

        def id(self):
		"""compute unique identifier of the state,
                used for gathering state/action statistics"""
                if self.idmemo is None:
                        n = 0
                        for c in self.colors:
                                n = n*3 + c
                        self.idmemo = n
                return self.idmemo
			
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
                        self[stateid] = dict((move, MoveStat()) \
				           for move in state.availableMoves())
                return dict.__getitem__(self, stateid)

class Game:
        
        """Simulate an sos game.
        
        methods:
        initialState() -- return a new sos game.
        scoreBonus(state) -- receive a sos game state and return the score bonus of the game.
        """
        
        def __init__(self, n, values = None, order = 'r', scorebonus = 0):
                """initiate sos game of a given size.
                
                receive:
                n -- game size
                values -- values of moves (optional)
                order -- order of moves' values
		score_bonus -- how to compute the players' scores"""
                self.n = n
		self.score_bonus = scorebonus
                self.values = values or self.__initValues(order)
                
        def __initValues(self, order):
                """initiate moves' values according to a given order"""
                values = range(self.n)
                if order == 1:    # ascending
                        pass # already in accending order
                elif order == 2:  # descending
                        values.reverse()  
                elif order == 0:  # random
                        shuffle(values)
                return values
        
        def __initialState(self):
                """create an initial state of the game"""
                return State(self.n)
                
        def isFinalState(self, state):
                return not state.availableMoves()
        
        def play(self, firstPlayer, secondPlayer):
                """simulate a game for two players"""
                state = self.__initialState()
                while not self.isFinalState(state):
                        move = firstPlayer.selectMove(state)
                        state.whiteMove(move)
                        move = secondPlayer.selectMove(state)
			state.blackMove(move)
                return self.calcScore(state)        
	
        def __score(self, indices):
                """return total score of switches at the indices"""
                return sum(self.values[i] for i in indices)
        
        def scoreBonus(self, state):
                """compute game score bonus"""
                return self.__score(state.whites()) - self.__score(state.blacks())
	
        def winloss(self, state):
		"""return 1 if first player won and -1 otherwise"""
		if self.scoreBonus(state) >= self.n/2:
			return 1
		else: 
			return -1
	
	def calcScore(self, state):
		"""return the first player's score.
		The second player score is it's negation"""
		if self.score_bonus:
			return self.scoreBonus(state)
		else:
			return self.winloss(state)

class Agent:
        """abstract agent"""

        def __init__(self, game):
                self.game = game

        def selectMove(self, state):
                """select move based on the state of the game"""
                assert False, "selectMove not implemented for %s" % \
                    self.__class__
	
	@classmethod
	def name(self):
		return self.__name__

def test_game():
        game = Game(4, [3, 2, 0, 1])
        state = State(4)
        state.whiteMove(2)
        state.blackMove(0)
        state.whiteMove(1)
        state.blackMove(3)
        assert game.calcScore(state) == -1
         
        
def test_turn():
	state = State(4)
	assert state.isWhiteTurn()
	state.whiteMove(3)
	assert not state.isWhiteTurn()
	state.blackMove(2)
	assert state.isWhiteTurn()	
	
	
def test_availableMoves():
        state = State(4)
        assert state.availableMoves()==[0, 1, 2, 3]

        state.whiteMove(2)
        state.blackMove(0)
        assert state.availableMoves()==[1,3]

def test_isFinal():
        game = Game(4)
        state = State(4)
        
        state.whiteMove(2)
        state.blackMove(0)
        assert not game.isFinalState(state)
        
        state.whiteMove(1)
        state.blackMove(3)
        assert game.isFinalState(state)
        
def test_whites_blacks():
        state = State(4)
        
        state.whiteMove(2)
        state.blackMove(0)
        state.whiteMove(1)
        state.blackMove(3)
        assert state.whites()==[1,2]
        assert state.blacks()==[0,3]
        
def test_state_id():
        statea = State(32)
        stateb = State(32)
        statec = State(32)
        statea.whiteMove(2)
        statea.blackMove(30)
        stateb.whiteMove(2)
        stateb.blackMove(30)
        statec.blackMove(2)
        statec.whiteMove(30)
        assert id(statea) != id(stateb) \
            and statea.id()==stateb.id() \
            and statea.id()!=statec.id()

def test_state_copy():
        statea = State(4)
        statea.whiteMove(3)
        statea.blackMove(1)
        stateb = copy(statea)
        movesa = statea.availableMoves()
        movesb = stateb.availableMoves()
        assert 2 == len(movesb)
        for i in range(2):
                assert movesa[i] == movesb[i]
        
def test_state():
        test_availableMoves()
        test_isFinal()
        test_whites_blacks()
        test_state_id()
        test_state_copy()
	test_turn()
        
def test():
        test_state()
        test_game()
        
test()
        
