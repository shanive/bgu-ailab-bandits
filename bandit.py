from random import random

class Arm:
	"simulation of bendit's arm"

	def __init__(self, average):
		self.average = average

	def pull(self):
		"""returns the result (1/0)"""

		if random()<self.average :
			return 1
		else:
			return 0
	
	def getAverage(self):
		"""returns the arm's average"""
		return self.average

class Bandit:
	"simulation of a bandit"

	def __init__(self, averageList):
		#initialize bandit's arms
		self.arms = [Arm(average) for average in averageList]
		#calculate the best arm average:
		self.bestArmAverage = max(averageList)
		

	def pullArm(self, armNum):
		"""pulls the bandit's arm in the given index"""
		return self.arms[armNum].pull()
	
	def getArmsNum(self):
		"""returns the numbers of arm in bandit"""
		return len(self.arms)
	
	def calcRegret(self, armIndex):
		"""returns the regret of the arm in the given index"""
		regret = self.bestArmAverage - self.arms[armIndex].getAverage()
		return regret

def _test_arm():
	one = Arm(2)
	zero = Arm(-1)
	assert one.getAverage() == 2
	assert one.pull()==1
	assert zero.pull()==0
	
def _test():
	_test_arm()
	
_test()

if __name__ == "__main__":
	averages = [0.4, 0.7, 0.1, 0.6]
	semiBandit = Bandit(averages)
	
	for i in range(0, 4):
		print str(semiBandit.calcRegret(i))
		#print str(semiBandit.pullArm(i))


