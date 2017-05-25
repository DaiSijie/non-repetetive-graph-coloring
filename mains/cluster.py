import os, sys, inspect
import Queue
from time import gmtime, strftime
import time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.solver import solveForEdges
from helpers.paths import allPaths
from helpers.SeparatePathsFinder import SeparatePathsFinder
from gurobipy import *

treeAnalyzed = 0
caterpillar = 0

#hard-coded user constants
caterpillarON = True
maxCliqueON = True
luckyPunchON = True

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
  fwdmap = dict()
  for e in E:
    if e in largestEdgeClique:
      largestClique.add(sizel)
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

  return (sizel, El, largestClique, fwdmap)

def isFeasible(paths, assignment):
  for p in paths:
    length = len(p)
    if length % 2 == 0:
      noDiff = True
      for i in xrange(length/2):
        noDiff = noDiff and assignment[p[i]] == assignment[p[i + length/2]] 
      if noDiff:
        return False
  return True      

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

  if caterpillarON:
    #Check for caterpillar:
    #They are the trees in which every vertex of degree at least three has at most two non-leaf neighbors.
    for i in xrange(size):
      if degrees[i] >= 3:
        count = 0 #count non-leaf neighbors. v is non-leaf iff it has degree >= 2
        for n in neighbors[i]:
          if degrees[n] >= 2:
            count += 1
        if count > 2:
          return (E, False, max(degrees), largestEdgeClique)
    caterpillar += 1
    return (E, True, max(degrees), largestEdgeClique)
  else:
    return (E, False, max(degrees), largestEdgeClique)

def verifyConjecture(rawInput, size):

  (E, isCaterpillar, maxDegree, largestEdgeClique) = fromTreeFlow(rawInput, size)

  if caterpillarON and isCaterpillar:
    return True

  upperBound = min(4 * maxDegree - 4, len(E))

  #compute the thue index of T
  (feasible, n, ass) = solveForEdges(E, upperBound, treePaths(size, E), largestEdgeClique) if maxCliqueON else solveForEdges(E, upperBound, treePaths(size, E))

  #try to color the line graph with n + 1 colors
  (sizel, El, largestClique, fwdmap) = lineGraph(size, E, largestEdgeClique) if maxCliqueON else lineGraph(size, E)
  
  suuu = SeparatePathsFinder(sizel, El)
  paths = suuu.popEverything()

  if luckyPunchON:
    #try to build lucky edge coloring:
    for e in E:
      luckyPunch = [0] * len(E)
      for ee in E:
        l = list(ee)
        a = max(l[0], l[1])
        b = min(l[0], l[1])
        if ee == e:
          luckyPunch[fwdmap[(a, b)]] = 999 #The special color
        else:
          for ((aa,bb), c) in ass:
            if a == aa and b == bb:
              luckyPunch[fwdmap[(a, b)]] = c
              break
            if isFeasible(paths, luckyPunch):
              return True

    #If no lucky punch worked, go the classical way
    #print "\n\n NO LUCKY PUNCH WORKED! \n\n"
  
  (feasible2, n2, ass2) = solve(sizel, n + 1, paths, largestClique)

  return feasible2


def printToLog(where, s):
  f = open(where + "/cluster.log", "aw+")
  date = strftime("%d %b %Y %H:%M:%S", gmtime())
  f.write(date + "] " + s + "\n")
  f.close()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python treeNRGC.py foldername\""
  else:
    offsetFile = int(sys.argv[2] if len(sys.argv) > 3 else 0)
    offsetLine = int(sys.argv[3] if len(sys.argv) > 3 else 0)
    folderName = sys.argv[1]
    printToLog(folderName, "Started running in " + folderName + " at file " + str(offsetFile) + " and line " + str(offsetLine))
    
    print "============= SETTINGS =============="
    print "maxCliqueON:   " + str(maxCliqueON)
    print "caterpillarON: " + str(caterpillarON)
    print "luckyPunchON:  " + str(luckyPunchON)
    print "====================================="

    globaly = True
    start = time.time()
    fileCounter = -1

    for name in os.listdir(folderName):
      if name[0] == "." or name == "cluster.log":
        continue #mac messes up with DS_STOREs

      #check if file was already tested
      fileCounter += 1
      if fileCounter < offsetFile:
        continue

      #retrieve info of file
      path = folderName + "/" + name
      name = name[4:]
      name = name[:len(name) - 4]
      name = name.split(".")
      size = int(name[0])
      radius = int(name[1])
      printToLog(folderName, "Start testing for file with size = " + str(size) + " radius = " + str(radius))

      lines = [line.rstrip('\n') for line in open(path)]
      holds = True
      counter = 1
      for l in lines:
        if counter < offsetLine:
          counter += 1
          continue
        if counter % 100 == 0:
          printToLog(folderName, "100 trees tested, counter = " + str(counter) + " holds? " + str(globaly))
        sys.stdout.write("\rTesting tree of size " + str(size) + " and radius " + str(radius) + ": " + str(counter) + "/" + str(len(lines)))
        sys.stdout.flush()
        holds = holds and verifyConjecture(l, size)
        if not holds:
          printToLog(folderName, " !!! CONJECTURE FALSE !!! at counter: " + str(counter))
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

    printToLog(folderName, "Done for this size. Results:\n============== RESULTS ==============\nConjecture holds:  " + str(globaly) +"\n " + "Tree analyzed:     " + str(treeAnalyzed)+" \n" + "Caterpillar found: " + str(caterpillar) + "\n" + "Time used:         " + str(end - start) + "\n" + "=====================================")



