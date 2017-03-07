import sys
import math
import Paths
import Solver
from gurobipy import *

def displayResults(n, assignment, backwardMap):
  print "\n========== RESULTS =========="
  
  print "Number of colors used: " + str(int(n))
  
  for v in xrange(len(assignment)):
    print "Vertex "+str(backwardMap.get(v))+": "+str(assignment[v])

  print "============================="


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


def construct(n):
  E = set()

  nvertices = n * n
  for i in xrange(n):
    for j in xrange(n):
      for k in xrange(j+1, n):
        E.add(frozenset([n * i + j, n * i + k]))

  for j in xrange(n):
    for i in xrange(n):
      for k in xrange(i + 1, n):
        E.add(frozenset([i * n + j, k * n + j]))

  return n






if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python GeneralNRGC.py graphFile\""
  else:
    f = open(sys.argv[1])
    (size, E, forwardMap, backwardMap) = fromEasyGraphFlow(f.read())
    (colors, assignment) = Solver.solve(size, 8, Paths.allPaths2(size, E))
    displayResults(colors, assignment, backwardMap)
