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


def hypothesis1(size, E, bckmap, k):
	s = SeparatePathsFinder(size, E)
	next = s.next()
	while len(next) > 0:
		print "checking paths of length: " + str(len(next[0]))
		yes = True
		for p in next:			
			indices = map(lambda x: toIndex(x, bckmap), p)
			if not canRemoveAWiggle(indices, k):
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


def canRemoveAWiggle(seq, k):
	s = len(seq) // 2


	#distance check:
	for i in xrange(s):
		if abs(seq[i] - seq[i + s]) <= 2*k:
			return True

	#Detect wiggle points
	wiggles = list()
	neig = list()
	for i in xrange(1, len(seq)-1): #Last and first cannot be wiggle (let's say)
		left = seq[i - 1]
		right = seq[i + 1]
		if left < seq[i] and seq[i] > right:
			wiggles.append(i)
			#Faulty neighbor
			if abs(seq[i] - left) < k:
				neig.append(i-1)
			elif abs(seq[i] - right) < k:
				neig.append(i+1)
			else:
				print "WARNING! THIS SHOULD NOT HAPPEN!!!"



	if len(wiggles) == 0:
		return True

	for w in wiggles:
		dual = w + s if w < s else w - s
		sub = popAtLoc(seq, [w, dual])
		if checkAxiomC(sub, k):
			return True
	
	for w in neig:
		dual = w + s if w < s else w - s
		sub = popAtLoc(seq, [w, dual])
		if checkAxiomC(sub, k):
			return True

	#try fusion
	for i in xrange(len(wiggles)):
		a = wiggles[i]
		b = neig[i]
		aa = a + s if a < s else a - s
		bb = b + s if b < s else b - s
		sub = popAtLoc(seq, [a,b,aa,bb])
		if checkAxiomC(sub, k):
			return True


	#Try exhaustive search
	print "Doing exhaustive search for " + str(seq)
	for t in powerset(range(s)):
		sub = popAtLoc(seq, t)
		if checkAxiomC(sub, k) and checkAxiomBD(sub, k):
			print "--> Working subset: " + str(t)
			return True

	return False


def existsSatSub(seq, k):
	s = len(seq) // 2
	for t in powerset(range(s)):
		sub = popAtLoc(seq, t)
		if checkAxiomC(sub, k) and checkAxiomBD(sub, k):
			print "--> Working subset: " + str(t)
			return True

	return False

def powerset(bag):
	toReturn = list()
	for i in xrange(1, 2 ** len(bag)):
		f = "{0:b}".format(i)
		while len(f) < len(bag):
			f = "0" + f
		toInsert = list()
		for i in xrange(len(bag)):
			if f[i] == '1':
				toInsert.append(bag[i])
		toReturn.append(toInsert)
	return toReturn
		
def checkAxiomBD(seq, k):
	vmin = min(seq)
	imin = -1
	for i in xrange(len(seq)):
		if seq[i] == vmin:
			if imin != -1:
				return False #Not unique!
			else:
				imin = i


	for i in xrange(1, len(seq)):
		left = seq[i - 1]
		if i <= imin and left < seq[i]:
			return False
		if i >= imin and left > seq[i]:
			return False

	return True

def checkAxiomC(seq, k):
	for i in xrange(len(seq) - 1):
		if abs(seq[i] - seq[i + 1]) > k:
			return False
	return True

def popAtLoc(seq, locs):
	toReturn = list()
	for i in xrange(len(seq)):
		if not (i in locs):
			toReturn.append(seq[i])
	return toReturn



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
		
		#print powerset([1,2,3])

		#exit()



		seq = [0, 2, 1, 3, 4, 6, 8, 10, 12, 14, 16, 15]
		print "exists? " + str(existsSatSub(seq, 2))

		exit()


		S = buildHardcoreString(2,5)
		





		for n in xrange(5, 9999):
			faulty = list(xrange(0, 2*n + 1, 2))
			faulty.append(2*n + 2)
			faulty.append(2*n + 1)

			repetitive = True
			l = len(faulty)//2
			for i in xrange(l):
				repetitive = repetitive and (S[faulty[i]] == S[faulty[i+l]])
			if repetitive:
				print "found!"

		print ":("

		exit()




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
		(sizel, El, bckmap, fwdmap) = lineGraph(size, E)
		print "hypothesis 1 is: " + str(hypothesis1(sizel, El, bckmap, k))

		#print E




		#S = buildHardcoreString(k, 5)

		#coloring = hotPunch(sizel, bckmap, S)




		#print "Conjecture is: " + str(coloringOk(sizel, El, coloring, bckmap, k))


