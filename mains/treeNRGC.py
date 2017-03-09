import os, sys, inspect
import Queue
import copy
from time import time



currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.solver import solveForEdges
from helpers.paths import allPaths2
from helpers.paths import allPaths1
from gurobipy import *

#Comment: this method is approximatively two times faster than networkx and ten times faster than the naive
def allPaths(size, E):
  toReturn = []
  for s in xrange(size - 1): #Last vertex will have been covered by everything
    toReturn.extend(allPathsFromS(size, E, s))
  return toReturn

##Should only returns paths to vertex > s
def allPathsFromS(size, E, s):
  toReturn = []
  visited = set()
  toVisit = Queue.Queue()
  toVisit.put((s, [s]))
  while not toVisit.empty():
    (visiting, how) = toVisit.get()
    visited.add(visiting)
    for n in xrange(size):
      if n not in visited and {visiting, n} in E:
        nhow = list(how)
        nhow.append(n)
        toVisit.put((n, nhow))
        if s < n and len(nhow) % 2 == 0:
          toReturn.append(nhow)
  return toReturn

def lineGraph(size, E):
  #First, we convert each edge to a number
  counter = 0
  bckmap = dict()
  for e in E:
    l = list(e)
    a = max(l[0], l[1])
    b = min(l[0], l[1])
    bckmap[counter] = (a, b)
    counter = counter + 1

  #Now, we build the new edge set:
  Ep = set()
  for i in xrange(counter):
    for j in xrange(i + 1, counter):
      (a1, a2) = bckmap[i]
      (b1, b2) = bckmap[j]
      if a1 == b1 or a1 == b2 or a2 == b1 or a2 == b2:
        Ep.add(frozenset([i, j]))

  return (counter, Ep)

def fromTreeFlow(rawInput):
  edgeList = rawInput.split("  ")

  E = set()
  for e in edgeList:
    v1 = int(e.split(" ")[0])
    v2 = int(e.split(" ")[1])
    E.add(frozenset([v1, v2]))

  return E

def fromEasyGraphFlow(rawInput):
  parts = rawInput.split(":")
  vertexList = parts[1].split(";")
  edgeList = parts[2].split(";")

  forwardMap = dict()
  backwardMap = dict()
  counter = 0
  for v in vertexList:
    forwardMap[v] = counter
    backwardMap[counter]  = v
    counter = counter + 1

  E = set()
  for e in edgeList:
    v1 = e.split(",")[0]
    v2 = e.split(",")[1]
    E.add(frozenset([forwardMap.get(v1), forwardMap.get(v2)]))

  size = len(vertexList)

  return (size, E, forwardMap, backwardMap)

def displayResults(n, assignment):
  print "\n========== RESULTS =========="
  
  print "Number of colors used: " + str(int(n))
  
  for v in xrange(len(assignment)):
    print "Vertex "+str(v)+": "+str(assignment[v])

  print "============================="

def displayEdgeResults(n, assignment, backwardMap):
  print "\n========== RESULTS =========="
  
  print "Number of colors used: " + str(int(n))
  
  for ((a,b), c) in assignment:
    print "Edge {" + str(backwardMap.get(a)) + ", " + str(backwardMap.get(b)) + "}: " + str(c)

  print "============================="


def verifyConjecture(rawInput, n):
  paths = Paths.allPaths(n, fromTreeFlow(rawInput))
  displayResults(*Solver.solve(n, n, paths))


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python TreeNRGC.py treeFile\""
  else:
    f = open(sys.argv[1])
    (size, E, forwardMap, backwardMap) = fromEasyGraphFlow(f.read())
    (n, ass) = solveForEdges(E, len(E), allPaths2(size, E))
    displayEdgeResults(n, ass, backwardMap)

    (nn, EE) = lineGraph(size, E)
    print "nn = "+str(nn)
    print EE

    #t1 = time()
    #paths = allPaths(size, E)
    #t2 = time()
    #paths2 = filter(lambda x: len(x) % 2 == 0, allPaths2(size, E))
    #t3 = time()
    #paths3 = filter(lambda x: len(x) % 2 == 0, allPaths1(size, E))
    #t4 = time()

    #print "time with optimized: " + str(t2-t1)
    #print "time with networkx: " + str(t3-t2)
    #print "time with naive: " + str(t4 - t3)
    #print "paths found with optimized: " + str(len(paths))
    #print "paths found with networkx: " + str(len(paths2))
    #print "paths found with naive: " + str(len(paths3))


    #print "number of vertices: "+str(size)
    #print "number of paths: "+str(len(paths))
    #for p in paths:
    #  pp = map(lambda x: backwardMap.get(x), p)
    #  print pp



    #lines = [line.rstrip('\n') for line in open(sys.argv[1])]
    #for l in lines:
    #   verifyConjecture(l, 7)

