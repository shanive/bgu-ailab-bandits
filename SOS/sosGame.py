import sos

class SOSGame:
	
	'Simulation of SOS game between two players'
	
	def __init__(self, firstplayer, secondplayer, n):
		"""receives two players and even number n a initial a game.
		firstplayer starts to play first"""
		self.white = firstplayer
		self.black = secondplayer
		self.__sos  = sos.SOS(n)
		
	def newGame(self):
		"""simulate a new sos game between the two players"""
		self.__sos.newGame()
		turns = self.__sos.getn()/2
		
		for i in range(0,turns):
				move = self.white(self.__sos.availableMoves())
				self.__sos.whiteMove(move)
				move = self.black(self.__sos.availableMoves())
				self.__sos.blackMove(move)
		return self.__sos.endGame()
		 
	
	def restart(self):
		"""start over the game"""
		self.__sos.restartGame()
		
	def changeSize(self, n):
		"""starts a new game with size n"""	
		self.__sos = sos.SOS(n)
	