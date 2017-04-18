import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from helpers.solver import solve
from helpers.SeparatePathsFinder import SeparatePathsFinder

import networkx as nx

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

def isSeparate(path, dim):
  bag1 = set()
  bag2 = set()

  l = len(path) / 2
  for i in xrange(1, l-1):
    e = path[i]
    column = e % dim + dim
    row = e // dim
    bag1.add(column)
    bag1.add(row)

  for i in xrange(1, l-1):
    e = path[i + l]
    column = e % dim + dim
    row = e // dim
    bag2.add(column)
    bag2.add(row)

  isSeparate = len(bag1.intersection(bag2)) == 0

  return isSeparate

def allPaths(n, E, dim, cutoff = None):
  G = nx.Graph()
  G.add_nodes_from(xrange(n))
  for e in E:
    ee = list(e)
    G.add_edge(ee[0], ee[1])

  paths = []
  for v1 in xrange(n):
    for v2 in xrange(v1 + 1, n):
      for p in nx.all_simple_paths(G, v1, v2, cutoff):
        if len(p) % 2 == 0 and isSeparate(p, dim):
          paths.append(p)
  return paths

def cord2int(x, y, dim):
  return dim * x + y

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print "Usage: \"python multigridNRGC.py dim lim\""
  else:
    dim = int(sys.argv[1])
    lim = int(sys.argv[2])

    E = buildMultigrid(dim)
    
    s = SeparatePathsFinder(dim * dim, E)
    paths = list()
    c = s.next()
    while len(c) > 0:
      if len(c[0]) <= lim:
        paths.extend(c)
        c = s.next()
      else:
        c = list()

    print "path done!"

    clique = set()
    for i in xrange(dim):
      clique.add(cord2int(i, 0, dim))

    (feasible, n, assignment) = solve(dim * dim, dim * dim, paths, clique)



    print "model solved"

    print "pi_"+str(lim)+"(M_"+str(dim)+") = "+str(n)
