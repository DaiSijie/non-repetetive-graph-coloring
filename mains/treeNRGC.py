import os, sys, inspect
import Queue
import time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.solver import solveForEdges
from helpers.paths import allPaths
from gurobipy import *

treeAnalyzed = 0
caterpillar = 0

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

def lineGraph(size, E, largestEdgeClique = set()):
  largestClique = set()

  #First, we convert each edge to a number
  sizel = 0
  bckmap = dict()
  for e in E:
    if e in largestEdgeClique:
      largestClique.add(sizel)
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

  return (sizel, El, largestClique)

def fromTreeFlow(rawInput, size):
  global treeAnalyzed
  global caterpillar

  edgeList = rawInput.split("  ")

  degrees = [0] * size
  neighbors = []
  for i in xrange(size):
    neighbors.append(set())

  E = set()
  for e in edgeList:
    v1 = int(e.split(" ")[0])
    v2 = int(e.split(" ")[1])
    E.add(frozenset([v1, v2]))
    neighbors[v1].add(v2)
    neighbors[v2].add(v1)
    degrees[v1] += 1
    degrees[v2] += 1

  largestEdgeClique = set()
  index = -1
  maxDegree = 0
  for i in xrange(size):
    if degrees[i] > maxDegree:
      maxDegree = degrees[i]
      index = i

  for e in E:
    if index in e:
      largestEdgeClique.add(e)

  treeAnalyzed += 1

  #Check for caterpillar:
  #They are the trees in which every vertex of degree at least three has at most two non-leaf neighbors.
  for i in xrange(size):
    if degrees[i] >= 3:
      count = 0 #count non-leaf neighbors. v is non-leaf iff it has degree >= 2
      for n in neighbors[i]:
        if degrees[n] >= 2:
          count += 1
      if count > 2:
        return (E, False, max(degrees))
  
  caterpillar += 1
  return (E, True, max(degrees), largestEdgeClique)

def verifyConjecture(rawInput, size):

  (E, isCaterpillar, maxDegree, largestEdgeClique) = fromTreeFlow(rawInput, size)

  if isCaterpillar:
    return True

  upperBound = min(4 * maxDegree - 4, len(E))

  #compute the thue index of T
  (feasible, n, ass) = solveForEdges(E, upperBound, treePaths(size, E), largestEdgeClique)

  #try to color the line graph with n + 1 colors
  (sizel, El, largestClique) = lineGraph(size, E, largestEdgeClique)
  (feasible2, n2, ass2) = solve(sizel, n + 1, allPaths(sizel, El), largestClique)

  return feasible2


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python treeNRGC.py folername\""
  else:
    folderName = sys.argv[1]
    globaly = True
    start = time.time()
    
    for name in os.listdir(folderName):
      if name[0] == ".":
        continue #mac messes up with DS_STOREs
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

    end = time.time()

    print "============== RESULTS =============="
    print "Conjecture holds:  " + str(globaly)
    print "Tree analyzed:     " + str(treeAnalyzed)
    print "Caterpillar found: " + str(caterpillar)
    print "Time used:         " + str(end - start)
    print "====================================="


