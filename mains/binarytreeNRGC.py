import math, os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solveForEdges
from helpers.solver import solve
from helpers.paths import allPaths

def buildBinaryTree(level):
	#labeling per level, from left to right, parent is always ceil(n/2) -  1
	size = 2**(level + 1) - 1
	E = set()
	for i in xrange(1, size):
		parent = int(math.ceil(i/2) - 1)
		E.add(frozenset([i, parent]))

	return (size, E)

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python binarytreeNRGC.py level\""
  else:
    level = int(sys.argv[1])

    (size, E) = buildBinaryTree(level)
    paths = allPaths(size, E)

    (feasible1, n1, ass1) = solveForEdges(E, 8, paths)
    print "Thue index: " + str(n1)
    (feasible2, n2, ass2) = solve(size, 4, paths)
    print "Thue number: " + str(n2)