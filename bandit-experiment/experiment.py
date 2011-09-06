 #!/usr/bin/python
 #argecho.py
import sys 
import bandit
import random
import algorithms
import logging
import getopt
import ../results-plot/plotCreator


def usage():
	"""prints the usage message"""
 	print "Usage: python <exp.py> --min <min-pulls> --max <max-pulls> --step <pull-step> --repeat <repetitions> --plot <bandit.txt> <algorithm-name> [algorithm-name]..."

 
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
 
def experimentFunc(pullsNum, algoname, bandit):
	"""excecute the experiment with pullsNum number of arm pulls according to the given algorithm.
	returns the index of the best arm"""
	
	algorithm = getattr(algorithms, algoname) 
	 
	resultsList = [[] for i in range(bandit.getArmsNum())] # the results of the pulls of every arm.
	 
	for pull in range (0, int(pullsNum)):
		
		arm = algorithm(resultsList)
		
		pullResult = bandit.pullArm(arm)
			 
		#print "pull result: "+str(pullResult)	 
			 
		resultsList[arm].append(pullResult)
		
		#print "result list: " + str(resultsList)
		
	return findBestArm(resultsList)
	
def calcAverageRegret(pullsNum, repetitions, algorithms, bandit):
	""" execute experimentFunc for a given repetitions num and return the average regret"""
	# initialize sum of the regrets in all repetitions
	algoNum = len(algorithms)
	
	avgRegrets = [0.0 for algo in range(algoNum)] 	 
	# execute the experiment Function repetitions times
	for algo in range(algoNum):
		
		logging.info('executes the algorithm: %s', algorithms[algo]) 
		
		algoRegret = 0.0
		
		for repeat in range(repetitions):
			
			logging.info('Round number: %d.', repeat)
			
			bestArm = experimentFunc(pullsNum, algorithms[algo], bandit)
			
			regret = bandit.calcRegret(bestArm)
			
			#logging.debug('The best arm and its regret for this round: %d %f respectively.', (bestArm, regret)) 
			
			algoRegret += regret
			
		#calculate average regret
		avgRegrets[algo] = algoRegret / repetitions
		
		#logging.debug('The average regret of the algorithm %s: %f' % (algorithms[algo], avgRegret[algo]))
		
	return avgRegrets
	 
def printFirstLine(algorithms):
	"""prints the first line in table of results"""
	strToPrint = "%-20s " % "samples"
	for algo in algorithms:
		strToPrint += "%-10s " % algo
	print strToPrint
	
def printResult(samples, regrets):
	""" print the result in a table"""
	strToPrint = "%-20d " % samples
	for regret in range(len(regrets)):
		strToPrint += "%-10f " % regrets[regret]
	print strToPrint
	
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
	  
def experimentMainLoop(nimPulls,maxPulls, pullStep, repetitions, bandit, algorithms):
	"""the outer loop of the experiment"""
	plotData = [["samples"]]+[[algoname] for algoname in algorithms]	# matrix of regrets
	
	pullsNum = minPulls
	
	logging.info('Start experiment.') 
	
	while pullsNum <= maxPulls:
		
		plotData[0].append(pullsNum)
		logging.info('Number of pulls: %f', pullsNum)
		avgRegret = calcAverageRegret(pullsNum, repetitions, algorithms, bandit)          #### todo ####
		
		for algo in range(1, len(plotData)):
			plotData[algo].append(avgRegret[algo - 1])
		
		printResult(pullsNum, avgRegret)
		
		pullsNum = pullsNum * pullStep 
		
	logging.info('Done experimant')
	
	return plotData
	
	
if __name__ == "__main__":
	 # arguments from command-line:
		
	logging.basicConfig(filename = 'experiment.log', level = logging.INFO)
	#defult values:	
	
	minPulls=10
	maxPulls=10000
	pullStep=2
	repeatitions=1000
	plot = False
		
	try:
        	opts, args = getopt.getopt(sys.argv[1:], "", ["min=", "max=", "step=", "repeat=", "plot"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '--min':
			minPulls = int(arg)
		elif opt == '--max':
			maxPulls = int(arg)
		elif opt == '--step':
			pullStep = float(arg)
		elif opt == '--repeat':
			repeatitions = int(arg)
		elif opt == '--plot'
			plot = True
			
	avgFileName = args[0]
	algoNames = args[1:] # may be few algorithms
	
	## arguments from file
	avgList = readAvgFromFile(avgFileName)
	bandit = bandit.Bandit(avgList)
		
	printFirstLine(algoNames)
	
	plotData = experimentMainLoop(minPulls, maxPulls, pullStep, repeatitions, bandit, algoNames)
	
	if plot:
		plotcreator = plotCreator.PlotCreator()
		plotcreator.create(plotData, "plot.png")
		
 	
