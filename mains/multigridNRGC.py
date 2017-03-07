import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve

def allPaths(n, E, lim):
  if lim % 2 == 1:
    lim = lim-1

  paths = []
  for v1 in xrange(n):
    for v2 in xrange(v1 + 1, n):
      for path in allSTPaths(n, E, v1, v2, lim):
        if len(path) % 2 == 0:
          paths.append(path)

  return paths

def allSTPaths(n, E, s, t, lim):
	V = set(list(xrange(n)))
	V.remove(s)
	paths = rAllSTPaths(V, E, s, t, lim-1)
	for path in paths:
		path.append(s)
	return paths

def rAllSTPaths(V, E, s, t, remaining):
  toReturn = []
  if remaining == 0:
    return toReturn
  for v in V:
  	if {s, v} in E: #If we can move from s to the particular v
  		if v == t: #If we arrived at destination, we're good
  			toReturn.append([t])
  		else:
  			#prepare new graph
  			V2 = V.copy()
  			V2.remove(v)
  			paths = rAllSTPaths(V2, E, v, t, remaining-1)
  			for path in paths:
  				path.append(v)
  				toReturn.append(path)
  return toReturn

def buildMultigrid(dim):
  E = set()

  #row connections:
  for row in xrange(dim):
    for i in xrange(dim):
      for j in xrange(i + 1, dim):
        E.add(frozenset([cord2int(row, i, dim), cord2int(row, j, dim)]))

  #line connections:
  for line in xrange(dim):
    for i in xrange(dim):
      for j in xrange(i + 1, dim):
        E.add(frozenset([cord2int(i, line, dim), cord2int(j, line, dim)]))

  return E

def cord2int(x, y, dim):
  return dim * x + y

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print "Usage: \"python multigridNRGC.py dim lim\""
  else:
    dim = int(sys.argv[1])
    lim = int(sys.argv[2])

    E = buildMultigrid(dim)
    paths = allPaths(dim * dim, E, lim)
    print "All paths are computed"

    (n, assignment) = solve(dim * dim, dim * dim, paths)
    print "pi_"+str(lim)+"(M_"+str(dim)+") = "+str(n)
