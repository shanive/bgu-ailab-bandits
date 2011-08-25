### Bandit algorithms

"""Bandit algorithms

An algorithm receives a list of lists of pull outcomes
and returns the index of the next arm to pull. The implemented
algorithms are:

  UCB -- UCB1 (max_i xi+sqrt(2*log(n)/ni)
  greedy -- 0.5-greedy"""

from math import log, sqrt
from random import random, randrange

def mean(v):
	return sum(v)/len(v)

def UCB(stats):
	"""Upper Confidence Bounds 1"""
	k = len(stats)
	n = sum(len(s) for s in stats) # total number of pulls
	ibest = -1
	xbest = -1
	for i in range(k):
		s = stats[i]
		ni = len(s)
		if ni==0:     # if there is a completely unexplored arm,
			return i  # return the arm
		x = mean(s)+sqrt(2.0*log(n)/ni)
		if x>xbest: # otherwise, maximize the upper confidence bound
			xbest = x
			ibest = i
	return ibest

def greedy(stats):
	"""0.5-greedy: pull best arm with probability 0.5,
    rest of the arms with equal probability"""
	k = len(stats)
	imax = -1
	xmax = -1
    # find the best arm (arm with the highest sample mean)
	for i in range(k):
		s = stats[i]
		if len(s)==0:
				return i
		x = mean(s)
		if x > xmax:
			imax = i
			xmax = x
	if random()> 0.5*k/(k-1.0):
		return imax
	else:
		return randrange(k)
	
def _test_ucb():
	assert UCB([[1.0],[0.0]])==0
	assert UCB([[1.0]*100,[0.0]])==1

def _test():
	_test_ucb()

_test()
