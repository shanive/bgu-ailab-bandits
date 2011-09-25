"""simulation of games for testing"""

### 
import getopt
import sys
import model
import agents

def usage():
	"""prints usage message in case of missing arguments"""
	print "Usage: python play.py --order r/a/d --values <list-values> n repetitions player1 player2"
	
	
def parse(argList):
	"""receive size, players' names and repetitions number as input and begin the play"""
	
	#default values:
	order = 'r' 
	values = None
	
	try:
		opts, args = getopt.getopt(argList, "", ["order=", "values="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
		
	for opt,arg in opts:
		if opt == '--order' and arg in ('r','a','d'):
			order = arg
		elif opt == '--values':
			values = list(arg)
		
		else:
			print "Unvalid Option\n"
			usage()
			sys.exit(2) 
	
	game = model.Game(int(args[0]), values, order)
	
	firstPlayer = getattr(agents, args[2])(game)
	secondPlayer = getattr(agents, args[3])(game)
	
	play(game, int(args[1]), firstPlayer, secondPlayer)
	
	

	
def play(game, repeat, firstPlayer, secondPlayer):
	"""excecute a given play between two given player for a given num of times
	
	return average difference""" 
	
	diff = 0.0
	for i in range(repeat):
		diff += game.play(firstPlayer, secondPlayer)
	print "The average difference is: %f" %  (diff / repeat)



if __name__ == '__main__':
	
	parse(sys.argv[1:])
