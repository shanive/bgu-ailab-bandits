 #!/usr/bin/python
 
import bandit
import random
 
def myAlgo(resultList):
	""" receives a lists of arm pulling results and return a number of arm to pull
	just for testing"""
	 
	armsNum = len(resultList)-1
	rand = random.randint(0, armsNum)
	return rand
 
def findBestArm(resultsList):
	"""returns the average of the best arm according to results in resultsList"""
	bestAvg = -1
	for arm in range (len(resultsList)):
		if resultsList[arm]: 
			tempAvg = float(resultsList[arm].count(1)) / len(resultsList[arm]) #compute the average of the i'th arm.
			if tempAvg > bestAvg:
				bestAvg = tempAvg
	return bestAvg	
 
def experimentFunc(pullsNum, algorithem, bandit):
	"""excecute the experiment with pullsNum number of arm pulls according to the givem algorithem
	returns the average of the best arm"""

	 
	resultsList = [[] for i in range(bandit.getArmsNum())] # the results of the pulls of every arm.
	 
	for pull in range (0, pullsNum):
		arm = algorithem(resultsList)
		pullResult = bandit.pullArm(arm)	 
		resultsList[arm].append(pullResult)
	print str(resultsList)
	return findBestArm(resultsList)
	 
	
def printResult(pulls, regret):
	""" print the result in a table"""
	print repr(pulls).rjust(10), repr(regret).rjust(5) 
	  
	 
 
 ################ help functions ##############
 
 
if __name__ == "__main__":
	 # from command-line:
	 minPulls =  10              
	 maxPulls = 10
	 pullStep =  10
	 repetitions = 3
	 #algName =
	 ## from file
	 #averageList = 
	 bandit = bandit.Bandit([0.4, 0.7, 0.1, 0.6])             ####### for tests #######
	 print str(bandit.bestAvg())
	 #bestArm  = experimentFunc(10, myAlgo, bandit)
	 #print str(bestArm) 
	  
	 print  repr("samples").rjust(10), repr("regret").rjust(10)       ### first row in table
	 pullsNum = minPulls
	 while pullsNum <= maxPulls:
		 
		sumOfRegrets = 0 	#sum of the regrets in all repetitions 
		for repeat in range(repetitions):
			bestAvg = experimentFunc(pullsNum, myAlgo, bandit)
	 		regret = bandit.bestAvg() - bestAvg
			sumOfRegrets += regret
		avgRegret = float(sumOfRegrets) / repetitions
		printResult(pullsNum, avgRegret)
		pullsNum = pullsNum * pullStep 
		
 


 
