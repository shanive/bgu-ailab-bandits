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

class Bandit:
    "simulation of a bandit"

    def __init__(self, averageList):
        self.arms = [Arm(average) for average in averageList]

    def pullArm(self, armNum):
        """pulls the bandit's arm in the given index"""
        return self.arms[armNum].pull()


if __name__ == "__main__":
    averages = [0.4, 0.7, 0.1, 0.6]
    semiBandit = Bandit(averages)
    for i in range(0, 4):
        print str(semiBandit.pullArm(i))
    

