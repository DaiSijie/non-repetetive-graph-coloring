import sys
import math
import Solver
import Paths
from gurobipy import *

def fromTreeFlow(rawInput):
  edgeList = rawInput.split("  ")

  E = set()
  for e in edgeList:
    v1 = int(e.split(" ")[0])
    v2 = int(e.split(" ")[1])
    E.add(frozenset([v1, v2]))

  return E

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
    lines = [line.rstrip('\n') for line in open(sys.argv[1])]
    for l in lines:
        verifyConjecture(l, 7)

