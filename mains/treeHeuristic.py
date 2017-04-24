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


def coloringOk(size, E, coloring):
	s = SeparatePathsFinder(size, E)
	next = s.next()
	while len(next) > 0:
		print "checking paths of length: " + str(len(next[0]))
		for p in next:
			if pathRepetitive(p, coloring):
				return False
		next = s.next()
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

		nameEdges(0, -1, k, h)
		(size, E) = buildCompleteKTree(k, h)
		(sizel, El, bckmap, fwdmap) = lineGraph(size, E)

		S = buildString(k)

		coloring = hotPunch(sizel, bckmap, S)

		print "Conjecture is: " + str(coloringOk(sizel, El, coloring))


