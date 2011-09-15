from random import randint



class SOS:
	"Implementation of Sum Of Switches Game"
	
	def __init__(self, n):
		"""Initialize SOS game,
		receives the number of possible moves""" 
		self.__n = n
		##Create an array of n moves. each move is a number between 0 to n-1:
		self.__moves = [0 for i in range(n)]
		
		
			
	def newGame(self, algorithm):
		"""receive__s an algorithm to play the game
		return the winner: 1 for white and 0 for black"""
	
		self.__initMoves()		##initialize moves' values
			
		whiteScore = 0
		blackScore = 0
		
		whiteMoves, blackMoves = algorithm(self.__n)
		
		#compute white's score
		for move in whiteMoves:
			whiteScore += self.__moves[move]
		#compute black's score
		for move in blackMoves:
			blackScore += self.__moves[move]	
			
		k = round(self.__n / 2.0)
		if k > self.__n / 2.0:
			k -= 1 
		
		if whiteScore - blackScore >= int(k):
			return 1
		else:
			return 0
			
			
	def __initMoves(self):
				
		src = [i for i in range(self.__n)]
		
		##initialize the moves' values:
		for i in range(self.__n):
			rand = randint(0, self.__n-1-i)
			self.__moves[i] = src[rand]
			src[rand], src[self.__n-1-i] = src[self.__n-1-i], src[rand]	#swap
		

