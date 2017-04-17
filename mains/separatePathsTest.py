import os, sys, inspect, time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.paths import allPaths
from helpers.SeparatePathsFinder import SeparatePathsFinder

def naiveAllSeparatePaths(n, E, cutoff = None):
  neighbors = [set() for _ in xrange(n)]
    
  for e in E:
    (a, b) = (list(e)[0], list(e)[1])
    neighbors[a].add(b)
    neighbors[b].add(a)

  separatePaths = list()
  for p in allPaths(n, E):
    if len(p) % 2 == 0 and isSeparate(p, neighbors):
          separatePaths.append(p)
  return separatePaths

def isSeparate(p, neighbors):
  l = len(p)/2
  for i in xrange(l):
    for j in xrange(l):
      m = j + l
      areNeighbors = p[i] in neighbors[p[m]]
      if areNeighbors and not (i == 0 and m == 2*l-1) and not (i == l-1 and m == l):
        return False
  return True

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
    print "Usage: \"python separatePathsTest.py graphFile\""
  else:
    f = open(sys.argv[1])
    (size, E, forwardMap, backwardMap) = fromEasyGraphFlow(f.read())
    
    t1 = time.time()
    s = SeparatePathsFinder(size, E)
    r1 = s.popEverything()
    t2 = time.time()
    r2 = naiveAllSeparatePaths(size, E)
    t3 = time.time()

    print "Optimized time: " + str((t2 - t1)*1000)
    print "Naive time: " + str((t3 - t2)*1000)

    print r1
    print r2

    print "Same number of paths: " + str(len(r1) == len(r2))
