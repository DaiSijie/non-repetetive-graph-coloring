import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from gurobipy import *

def displayResults(feasible, n, assignment):
  print "\n========== RESULTS =========="
  
  print "Number of colors used: " + str(int(n))
  
  yeh = ""
  for v in xrange(len(assignment)):
    print "Vertex "+str(v)+": "+str(assignment[v])
    yeh = yeh + str(assignment[v])
  
  print "============================="
  print yeh


def generatePaths(size):
  paths = []
  for length in xrange(2, size + 1, 2): #All even-length in range 2..size
    for start in xrange(0, size - length + 1):
      p = []
      for v in xrange(length):
        p.append(v + start)
      paths.append(p)
  return paths

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python NRGC.py sizeOfPath\""
  else:
    size = int(sys.argv[1])
    displayResults(*solve(size, 3, generatePaths(size))) #The three here come from a result of Thue
