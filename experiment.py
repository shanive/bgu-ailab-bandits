 #!/usr/bin/python
 #argecho.py
import sys 
import bandit
import random
import algorithms
import logging
import getopt


def usage():
	"""prints the usage message"""
 	print "Usage: python <exp.py> --min <min-pulls> --max <max-pulls> --step <pull-step> --repeat <repetitions> <bandit.txt> <algorithm-name>"
	
def myAlgo(resultList):
	""" receives a lists of arm pulling results and return a number of arm to pull
	just for testing"""
	 
	armsNum = len(resultList)-1
	rand = random.randint(0, armsNum)
	return rand
 
def findBestArm(resultsList):
	"""returns the Index of the best arm according to results in resultsList"""
	bestAvg = -1
	bestArmIndex = -1
	for arm in range (len(resultsList)):
		if resultsList[arm]: 
			tempAvg = float(resultsList[arm].count(1)) / len(resultsList[arm]) #compute the average of the i'th arm according to results
			if tempAvg > bestAvg:
				bestAvg = tempAvg
				bestArmIndex = arm
	return bestArmIndex	
 
def experimentFunc(pullsNum, algorithm, bandit):
	"""excecute the experiment with pullsNum number of arm pulls according to the given algorithm.
	returns the index of the best arm"""
	 
	resultsList = [[] for i in range(bandit.getArmsNum())] # the results of the pulls of every arm.
	 
	for pull in range (0, pullsNum):
		
		arm = algorithm(resultsList)
		
		pullResult = bandit.pullArm(arm)
			 
		#print "pull result: "+str(pullResult)	 
			 
		resultsList[arm].append(pullResult)
		
		#print "result list: " + str(resultsList)
		
	return findBestArm(resultsList)
	
def calcAverageRegret(pullsNum, repetitions, algorithm, bandit):
	""" execute experimentFunc for a given repetitions num and return the average regret"""
	# initialize sum of the regrets in all repetitions
	sumOfRegrets = 0.0 	 
	# execute the experiment Function repetitions times
	for repeat in range(repetitions):
		
		logging.info('Round number: %d.', repeat)
		
		bestArm = experimentFunc(pullsNum, algorithm, bandit)
		
		regret = bandit.calcRegret(bestArm)
		
		logging.debug('The best arm and its regret for this round: %d %f respectively.', (bestArm, regret)) 
		
		sumOfRegrets += regret
		
	#calculate average regret
	avgRegret = float(sumOfRegrets) / repetitions
	
	return avgRegret
	 
def printFirstLine():
	"""prints the first line in table of results"""
	print "%-20s %-10s" % ("samples", "regret")
	
def printResult(pulls, regret):
	""" print the result in a table"""
	print "%-20d %-10f" % (pulls, regret)
	
def readAvgFromFile(fileName):
	"""returns a list of averages that was read from a given file"""
	banditFile = open(fileName, 'r')
	# string = banditFile.read()
	avgList = []
	
	logging.info('Reading from file.')
	
	for line in banditFile:
		avgList.extend([float(num) for num in line.split()])
	banditFile.close()
	
	logging.info('Done reading from file.')
	
	return avgList 
	  
def experimentMainLoop(nimPulls,maxPulls, pullStep, repetitions, bandit, algorithm):
	"""the outer loop of the experiment"""
	pullsNum = minPulls
	
	logging.info('Start experiment.') 
	
	while pullsNum <= maxPulls:
		
		logging.info('Number of pulls: %f', pullsNum)
		avgRegret = calcAverageRegret(pullsNum, repetitions, algorithm, bandit)          #### todo ####
		printResult(pullsNum, avgRegret)
		
		pullsNum = pullsNum * pullStep 
		
	logging.info('Done experimant')
	
	
#def parseCommandLineArg(argv, dict):
	#"""perse command line arguments"""
	#try:
        	#opts, args = getopt.getopt(argv, "", ["min=", "max=", "step=", "repeat="])
	#except getopt.GetoptError:
		#usage()
		#sys.exit(2)
	#for opt, arg in opts:
		#if opt == '--min':
			#dict['minPulls'] = arg
		#elif opt == 'max':
			#dict['maxPulls'] = arg
		#elif opt == '--step':
			#dict['pullStep'] = arg
		#elif opt == 'repeat':
			#dict['repeatitions'] = arg
	#dict['avgFileName'] = args[0]
	#dict['algoName'] = args[1]
		
			
	
if __name__ == "__main__":
	 # arguments from command-line:
		
	logging.basicConfig(filename = 'experiment.log', level = logging.INFO)
	#defult values:	
	#dict = {'avgFileName':'bandits.txt', 'minPulls':10 , 'maxPulls':10000, 'pullStep': 2, 'repeatitions':1000, 'algoName':'greedy'} 
	minPulls=10
	maxPulls=10000
	pullStep=2
	repeatitions=1000
		
	try:
        	opts, args = getopt.getopt(sys.argv[1:], "", ["min=", "max=", "step=", "repeat="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '--min':
			minPulls = int(arg)
		elif opt == 'max':
			maxPulls = int(arg)
		elif opt == '--step':
			pullStep = int(arg)
		elif opt == 'repeat':
			repeatitions = int(arg)
			
	avgFileName = args[0]
	algoName = args[1]
	
	## arguments from file
	avgList = readAvgFromFile(avgFileName)
	bandit = bandit.Bandit(avgList)
	algorithm = getattr(algorithms, algoName) 
		
	printFirstLine()
	
	experimentMainLoop(minPulls, maxPulls, pullStep, repeatitions, bandit, algorithm)
		
 
