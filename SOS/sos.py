from random import choice

class Move:
	"""Simulation of a move in SOS game.
	Every move has value and color.
	A move's color represents the move's state: gray = available, white = choosen by white player, black = choosen by black player"""
	def __init__(self, value, color):
		self.__value  = value
		self.__color = color
		
	def setValue(self, value):
		"""changes the move's value"""
		self.__value = value 
	
	def setColor(self, color):
		"""changes the move's color"""
		self.__color = color
		
	def getValue(self):
		return self.__value
	
	def getColor(self):
		return self.__color
		
class SOS:
	"Implementation of Sum Of Switches Game"
	
	def __init__(self, n):
		"""Initialize SOS game,
		receives the number of possible moves (even number)""" 
		self.__n = n
		
				# initial values for moves
		
		
	def getn(self):
		"""returns the number of moves"""
		return self.__n
	
	def restartGame(self):
		"""start a game with the same moves' values"""
		for move in self.__moves:
			move.setColor('gray')
		
			
	def newGame(self):
		"""starts a new game"""
		
		self.__moves = []
				
		src = [i for i in range(self.__n)]	#moves' values
		
		##initialize the moves' values:
		for i in range(self.__n):
			value = choice(src)		#choose value randomly for move number i
			move = Move(value, 'gray')
			self.__moves.append(move)
			src.remove(value)		#remove the value from values list to prevent duplicate values 
			
			
		
	def whiteMove(self, move):
		"""add a given move number to white player's moves"""
		self.__moves[move].setColor('white')
		
	def blackMove(self, move):
		"""add a given move number to black player's moves"""
		self.__moves[move].setColor('black')	

	
	def endGame(self):
		"""return the distance between the white player's score and the black player's score"""
		
		whiteScore = 0
		blackScore = 0
		
		for move in self.__moves:
			if move.getColor() == 'white':
				whiteScore += move.getValue() 	
			else:
				blackScore += move.getValue()
				
		return whiteScore - blackScore
	
	def availableMoves(self):
		"""returns a list of unchoosen moves"""
		grayMoves = []
		for i in range(self.__n):
			if self.__moves[i].getColor() == 'gray':
				grayMoves.append(i)
		return grayMoves
