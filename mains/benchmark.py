import os, sys, inspect, time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.paths import allPaths
from helpers.maximalClique import findMaximalClique
from helpers.SeparatePathsFinder import SeparatePathsFinder
from gurobipy import *

def benchmark(separatePaths, symmetryBreaking, treeOptimizations):
	
	print "================ SETTINGS ==============="
	print "SeparatePaths: " + str(separatePaths)
	print "SymmetryBreaking: " + str(symmetryBreaking)
	print "TreeOptimizations: " + str(treeOptimizations)
	print "========================================="

	graphs = list()
	names = list()

	graphs.append("version=1:1;a;2;b;3;c;4;d;5;e:a,1;2,1;5,1;c,a;d,a;b,2;3,2;d,b;e,b;c,3;4,3;e,c;d,4;5,4;e,5")
	names.append("Petersen")

	graphs.append("version=1:1;2;3;4;5;6;7;8;9:2,1;3,1;4,1;7,1;3,2;5,2;8,2;6,3;9,3;5,4;6,4;7,4;6,5;8,5;9,6;8,7;9,7;9,8")
	names.append("R33")

	graphs.append("version=1:11;12;13;14;15;0;1;2;3;4;5;6;7;8;9;10:3,11;15,11;7,11;8,11;9,11;13,12;14,12;4,12;15,12;8,12;14,13;15,13;5,13;9,13;2,14;15,14;6,14;3,15;7,15;12,0;1,0;2,0;3,0;4,0;8,0;13,1;2,1;3,1;5,1;9,1;3,2;6,2;7,3;5,4;6,4;7,4;8,4;6,5;7,5;9,5;7,6;9,8;11,10;2,10;14,10;6,10;8,10;9,10")
	names.append("R44")

	graphs.append("version=1:a;b;c;d;e;f;g;h;i;j:b,a;c,a;d,a;e,a;f,a;g,a;h,a;i,a;j,a;c,b;d,b;e,b;f,b;g,b;h,b;i,b;j,b;d,c;e,c;f,c;g,c;h,c;i,c;j,c;e,d;f,d;g,d;h,d;i,d;j,d;f,e;g,e;h,e;i,e;j,e;g,f;h,f;i,f;j,f;h,g;i,g;j,g;i,h;j,h;j,i")
	names.append("K10")

	print "================ RESULTS ================"
	t0 = time.time()
	ts = time.time()
	for i in xrange(len(graphs)):
		(size, E) = fromEasyGraphFlow(graphs[i])
		timeSolve(size, E, separatePaths, symmetryBreaking, treeOptimizations)
		print "For " + names[i] + ": " + str(time.time() - ts) + "s"
		ts = time.time()
	"Globally: " + str(time.time() - t0) + "s"
	print "========================================="


def timeSolve(size, E, separatePaths, symmetryBreaking, treeOptimizations):
	#First, we compute all paths
	paths = list()
	if separatePaths:
		s = SeparatePathsFinder(size, E)
		paths = s.popEverything()
	else:
		for p in allPaths(size, E):
			if len(p) % 2 == 0:
				paths.append(p)

	#Then, we might look for symmetry breaking with three restarts?!
	clique = set()
	if symmetryBreaking:
		clique = findMaximalClique(size, E, 3)

	#Then, we might perform treeOptimizations:
	if treeOptimizations:
		pass #ToDo
		#Check for tree

	solve(size, size, paths, clique)


def fromEasyGraphFlow(rawInput):
  parts = rawInput.split(":")
  vertexList = parts[1].split(";")
  edgeList = parts[2].split(";")

  forwardMap = dict()
  counter = 0
  for v in vertexList:
    forwardMap[v] = counter
    counter = counter + 1

  E = set()
  for e in edgeList:
    v1 = e.split(",")[0]
    v2 = e.split(",")[1]
    E.add(frozenset([forwardMap.get(v1), forwardMap.get(v2)]))

  size = len(vertexList)

  return (size, E)


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Usage: \"python benchmark.py separatePaths symmetryBreaking treeOptimizations\""
	else:
		separatePaths = sys.argv[1] == "t"
		symmetryBreaking = sys.argv[2] == "t"
		treeOptimizations = sys.argv[3] == "t"
		benchmark(separatePaths, symmetryBreaking, treeOptimizations)

