"""this module contain the class SOSGame"""
import sos

class SOSGame:
	
	'Simulation of SOS game between two players'
	
	def __init__(self, firstplayer, secondplayer, n, valOrder = 'r'):
		"""receive two players and even number n a initial a game."""
		self.white = firstplayer
		self.black = secondplayer
		self.game  = sos.Game(n, order = valOrder)
		
	def newGame(self):
		"""simulate a new sos game between the two players"""
		state = self.game.initialState()
		turns = self.game.n/2
		
		for i in range(turns):
				move = self.white(state.availableMoves())
				state.whiteMove(move)
				move = self.black(state.availableMoves())
				state.blackMove(move)
				
		return self.game.scoreBonus(state)
		 
	
	#def restart(self):
		#"""start over the game"""
		#self.__sos.restartGame()
		
	def changeSize(self, n, valOrder = 'r'):
		"""change the size of the game for a given value n and a given values' order valOrder (optional)"""	
		self.game = sos.Game(n, order = valOrder)
	