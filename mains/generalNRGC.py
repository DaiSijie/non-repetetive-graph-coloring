import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.solver import solveForEdges
from helpers.paths import allPaths
from helpers.SeparatePathsFinder import SeparatePathsFinder
from gurobipy import *

def displayEdgeResults(n, assignment, backwardMap):
  print "\n========== RESULTS =========="
  
  print "Number of colors used: " + str(int(n))
  
  for ((a,b), c) in assignment:
    print "Edge {" + str(backwardMap.get(a)) + ", " + str(backwardMap.get(b)) + "}: " + str(c)

  print "============================="


def displayResults(feasible, nOfColors, assignment, backwardMap):
  print "\n========== RESULTS =========="
  
  if not feasible:
    print "Model is infeasible"
  else:
    print "Number of colors used: " + str(nOfColors)
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

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python generalNRGC.py graphFile\""
  else:
    f = open(sys.argv[1])
    (size, E, forwardMap, backwardMap) = fromEasyGraphFlow(f.read())
    if len(sys.argv) == 3:
      (feasible, n, ass) = solveForEdges(E, len(E), allPaths(size, E)) #ToDo: improve lower bound for the number of colors
      displayEdgeResults(n, ass, backwardMap)
    else:
      (feasible, colors, assignment) = solve(size, size, SeparatePathsFinder(size, E))
      displayResults(feasible, colors, assignment, backwardMap)

