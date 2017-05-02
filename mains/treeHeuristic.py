import math

import os, sys, inspect
import Queue
import time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.solver import solveForEdges
from helpers.paths import allPaths
from helpers.SeparatePathsFinder import SeparatePathsFinder
from gurobipy import *


def coloringOk(size, E, coloring, bckmap, k):
	s = SeparatePathsFinder(size, E)
	next = s.next()
	while len(next) > 0:
		print "checking paths of length: " + str(len(next[0]))
		yes = True
		for p in next:			
			indices = map(lambda x: toIndex(x, bckmap), p)
			if pathRepetitive(p, coloring) or not indexingOk(indices, k):
				print "p = "
				for i in p:
					print toIndex(i, bckmap)
				return False
		next = s.next()
	return True

def toIndex(i, bckmap):
	(a,b) = bckmap[i]
	z = frozenset([a,b])
	return edgeNaming[z]

def indexingOk(seq, k):
	l = len(seq)//2
	for i in xrange(l):
		if abs(seq[i] - seq[i + l]) <= 2:
			return True

	#Find global minima, the turning point
	#m = 0
	#for s in len(seq):
	#	if seq[s] < seq[m]:
	#			m = s

	#Now, find wiggle points
	toRemove = [False] * (2 * l)
	for i in xrange(1, 2 * l - 1):
		left = seq[i - 1]
		right = seq[i + 1]
		if left < seq[i] and seq[i] > right:# and i != 2*l-2 and i != 1:
			toRemove[i] = True

	#Find dual index
	for i in xrange(l):
		if toRemove[i] or toRemove[i + l]:
			toRemove[i] = True
			toRemove[i + l] = True

	#Now, extract subsequence
	sub = list()
	for i in xrange(len(toRemove)):
		if not toRemove[i]:
			sub.append(seq[i])
	#print "original: " + str(seq) + " elidded: " + str(seq)

	#Perform distance check.
	for i in xrange(1, len(sub)):
		left = sub[i - 1]
		if abs(left - sub[i]) > k + 2:
			print "Faulty seq: " + str(seq)
			print "Ellided: " + str(sub)
			return False
	return True

def pathRepetitive(p, coloring):
	l = len(p)/2
	for i in xrange(l):
		if coloring[p[i]] != coloring[p[l + i]]:
			return False
	return True 

def hotPunch(sizel, bckmap, S):
	coloring = [0] * sizel
	for i in xrange(sizel):
		(parent, child) = bckmap[i]
		coloring[i] = S[edgeNaming[frozenset([parent, child])]]
	return coloring

edgeNaming = dict()

def nameEdges(parent, parentName, k, h):
	if h == 1:
		return
	else:
		for i in xrange(k):
			child = parent * k + 1 + i
			edgeNaming[frozenset([parent, child])] = parentName + 1 + i
			nameEdges(child, parentName + 1 + i, k, h - 1)

def buildString(k):
	yep = "2021020102101202120102012021201210120102120121012021201020120210120102012101202120102012021201210120" # precomputed thue sequence
	toReturn = list()
	for e in yep:
		for i in xrange(k + 1):
			toReturn.append(e + "_" + str(i))
	return toReturn

def buildHardcoreString(k, iterations):
	toReturn = "B"
	for i in xrange(iterations):
		ccp = ""
		for c in toReturn:
			if c == 'A':
				ccp = ccp + "BDAEAC"
			elif c == 'B':
				ccp = ccp + "BDC"
			elif c == 'C':
				ccp = ccp + "BDAE"
			elif c == 'D':
				ccp = ccp + "BEAC"
			elif c == 'E': 
				ccp = ccp + "BEAE"
		toReturn = ccp

	ccp = ""
	for c in toReturn:
		if c == 'A':
			ccp = ccp + "zuyxu"
		elif c == 'B':
			ccp = ccp + "zu"
		elif c == 'C':
			ccp = ccp + "zuy"
		elif c == 'D':
			ccp = ccp + "zxu"
		elif c == 'E': 
			ccp = ccp + "zxy"
	toReturn = ccp

	ccp = ""
	for c in toReturn:
		if c == 'x':
			ccp = ccp + "ca"
		elif c == 'y':
			ccp = ccp + "cb"
		elif c == 'z':
			ccp = ccp + "cab"
		elif c == 'u':
			ccp = ccp + "cba"
	toReturn = ccp

	tab = list()
	for c in toReturn:
		for i in xrange(k+1):
			if not (i == k and c == "c"):
				tab.append(c + "_" + str(i)) 

	return tab


def lineGraph(size, E):
  #First, we convert each edge to a number
  sizel = 0
  bckmap = dict()
  fwdmap = dict()
  for e in E:
    l = list(e)
    a = max(l[0], l[1])
    b = min(l[0], l[1])
    bckmap[sizel] = (a, b)
    fwdmap[(a,b)] = sizel
    sizel = sizel + 1

  #Now, we build the new edge set:
  El = set()
  for i in xrange(sizel):
    for j in xrange(i + 1, sizel):
      (a1, a2) = bckmap[i]
      (b1, b2) = bckmap[j]
      if a1 == b1 or a1 == b2 or a2 == b1 or a2 == b2:
        El.add(frozenset([i, j]))

  return (sizel, El, bckmap, fwdmap)


def buildCompleteKTree(k, h):
	size = (1 - (k**h))/(1 - k)
	E = set()
	for i in xrange(size - 1, 0, -1):
		parent = int(math.floor((i - 1)/k))
		E.add(frozenset([i, parent]))
	return (size, E)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: python treeHeuristic.py k h"
	else:
		k = int(sys.argv[1])
		h = int(sys.argv[2])

		print "k = " + str(k) + " h = " + str(h)


		#S = buildHardcoreString(2, 5)
		#print "Sle = " + str(len(S))

		#test
		#for i in xrange(0, 700, 2):
		#	toTest = [9, 7, 6, 5, 3, 4, 2, 0]
		#	for j in xrange(i):
		#		toTest.append(11 + i*2)
		#	#test for repetitiveness
		#	repetitive = True
		#	l = len(toTest)//2
		#	for i in xrange(l):
		#		repetitive = repetitive and (S[toTest[i]] == S[toTest[i+l]])
		#	if repetitive:
		#		print "found!"
		#print "hello"
		#exit()



		nameEdges(0, -1, k, h)
		(size, E) = buildCompleteKTree(k, h)

		print E

		(sizel, El, bckmap, fwdmap) = lineGraph(size, E)

		S = buildHardcoreString(k, 5)

		coloring = hotPunch(sizel, bckmap, S)

		print "Conjecture is: " + str(coloringOk(sizel, El, coloring, bckmap, k))


