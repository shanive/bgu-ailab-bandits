 #!/usr/bin/python
 #argecho.py
import sys 
import bandit
import random
import algorithms
 
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
		
		#print "the chosen arm is: "+str(arm)
		
		pullResult = bandit.pullArm(arm)
			 
		#print "pull result: "+str(pullResult)	 
			 
		resultsList[arm].append(pullResult)
		
		#print "result list: " + str(resultsList)
		
	return findBestArm(resultsList)
	
def calcAverageRegret(pullsNum, repetitions, algorithm, bandit):
	""" execute experimentFunc for a given repetitions num and return the average regret"""
	# initialize sum of the regrets in all repetitions
	
	#print "pulls number: " + str(pullsNum)
	
	sumOfRegrets = 0.0 	 
	# execute the experiment Function repetitions times
	for repeat in range(repetitions):
		bestArm = experimentFunc(pullsNum, algorithm, bandit)
		
		#print "best arm: " + str(bestArm)
		
		regret = bandit.calcRegret(bestArm)
		
		#print "regret: "+str(regret)
		
		sumOfRegrets += regret
		
		#print "sum of regrets: "+str(sumOfRegrets)
		
	#calculate average regret
	avgRegret = float(sumOfRegrets) / repetitions
	
	#print "average regret: "+str(avgRegret)
	
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
	for line in banditFile:
		avgList.extend([float(num) for num in line.split()])
	banditFile.close()
	return avgList 
	  
def experimentMainLoop(nimPulls,maxPulls, pullStep, repetitions, bandit):
	"""the outer loop of the experiment"""
	pullsNum = minPulls
	while pullsNum <= maxPulls:
		avgRegret = calcAverageRegret(pullsNum, repetitions, algorithms.greedy, bandit)          #### todo ####
		printResult(pullsNum, avgRegret)
		
		pullsNum = pullsNum * pullStep 

if __name__ == "__main__":
	 # arguments from command-line:
	if len(sys.argv) < 6:
		print "Usage: python <exp.py> <bandit.txt> <min-pulls> <max-pulls> <pull-step> <repetitions>"
		sys.exit(0)
	avgFileName = sys.argv[1]
	minPulls =  int(sys.argv[2])
	maxPulls = int(sys.argv[3])
	pullStep =  int(sys.argv[4])
	repetitions = int(sys.argv[5])
	## arguments from file
	avgList = readAvgFromFile(avgFileName)
	bandit = bandit.Bandit(avgList)
		
	printFirstLine()
	
	experimentMainLoop(minPulls, maxPulls, pullStep, repetitions, bandit)   
		
 


 
