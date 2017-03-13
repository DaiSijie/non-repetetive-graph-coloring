import os, sys, inspect
import Queue

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.solver import solveForEdges
from helpers.paths import allPaths
from gurobipy import *

#Comment: this method is approximatively two times faster than networkx and ten times faster than the naive
def treePaths(size, E):
  toReturn = []
  for s in xrange(size - 1): #Last vertex will have been covered by everything
    toReturn.extend(treePathsFromS(size, E, s))
  return toReturn

#Should only returns paths to vertex > s
def treePathsFromS(size, E, s):
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
        if s < n and len(nhow) % 2 == 1:
          toReturn.append(nhow)
  return toReturn

def lineGraph(size, E):
  #First, we convert each edge to a number
  sizel = 0
  bckmap = dict()
  for e in E:
    l = list(e)
    a = max(l[0], l[1])
    b = min(l[0], l[1])
    bckmap[sizel] = (a, b)
    sizel = sizel + 1

  #Now, we build the new edge set:
  El = set()
  for i in xrange(sizel):
    for j in xrange(i + 1, sizel):
      (a1, a2) = bckmap[i]
      (b1, b2) = bckmap[j]
      if a1 == b1 or a1 == b2 or a2 == b1 or a2 == b2:
        El.add(frozenset([i, j]))

  return (sizel, El)

def fromTreeFlow(rawInput):
  edgeList = rawInput.split("  ")

  E = set()
  for e in edgeList:
    v1 = int(e.split(" ")[0])
    v2 = int(e.split(" ")[1])
    E.add(frozenset([v1, v2]))

  return E

def verifyConjecture(rawInput, size):
  E = fromTreeFlow(rawInput)

  #compute the thue index of T
  (feasible, n, ass) = solveForEdges(E, len(E), treePaths(size, E)) #ToDo: improve lower bound for the number of colors
  print "n = "+str(n)

  #try to color the line graph with n + 1 colors
  (sizel, El) = lineGraph(size, E)
  (feasible2, n2, ass2) = solve(sizel, n + 1, allPaths(sizel, El))

  return feasible2

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python treeNRGC.py folername\""
  else:
    folderName = sys.argv[1]
    globaly = True
    for name in os.listdir(folderName):
      
      #retrieve info of file
      path = folderName + "/" + name
      name = name[4:]
      name = name[:len(name) - 4]
      name = name.split(".")
      size = int(name[0])
      radius = int(name[1])

      lines = [line.rstrip('\n') for line in open(path)]
      
      holds = True
      counter = 1
      for l in lines:
        sys.stdout.write("\rTesting tree of size " + str(size) + " and radius " + str(radius) + ": " + str(counter) + "/" + str(len(lines)))
        sys.stdout.flush()
        holds = holds and verifyConjecture(l, size)
        counter = counter + 1

      sys.stdout.write("\rTesting tree of size " + str(size) + " and radius " + str(radius) + ": conjecture is " + str(holds))
      sys.stdout.flush()
      print ""

      globaly = globaly and holds

    print "============ RESULTS ============"
    print "Conjecture holds: " + str(globaly)
    print "================================="

