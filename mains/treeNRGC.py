import os, sys, inspect
import Queue
import copy

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.paths import allPaths2
from gurobipy import *

def allPaths(size, E):
  toReturn = []
  for s in xrange(size):
    print "starting at: "+str(s)
    toReturn.extend(allPathsFromS(size, E, s))
  return toReturn

##Should only returns paths to vertex > s
def allPathsFromS(size, E, s):
  toReturn = []
  visited = set()
  toVisit = Queue.Queue()
  toVisit.put((s, [s]))
  while not toVisit.empty():
    print "While called! : toVisit size:::" + str(toVisit.qsize())
    (visiting, how) = toVisit.get()
    visited.add(visiting)
    for n in xrange(size):
      if n not in visited and {visiting, n} in E:
        nhow = copy.deepcopy(how)
        nhow.append(n)
        toVisit.put((n, nhow))
        if s < n:
          toReturn.append(nhow)
  return toReturn


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

def verifyConjecture(rawInput, n):
  paths = Paths.allPaths(n, fromTreeFlow(rawInput))
  displayResults(*Solver.solve(n, n, paths))


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python TreeNRGC.py treeFile\""
  else:
    f = open(sys.argv[1])
    (size, E, forwardMap, backwardMap) = fromEasyGraphFlow(f.read())
    paths = allPaths(size, E)
    print "number of vertices: "+str(size)
    print "number of paths: "+str(len(paths))
    for p in paths:
      pp = map(lambda x: backwardMap.get(x), p)
      print pp



    #lines = [line.rstrip('\n') for line in open(sys.argv[1])]
    #for l in lines:
    #   verifyConjecture(l, 7)

