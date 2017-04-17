import sys
import networkx as nx

def allPaths(n, E, cutoff = None):
  G = nx.Graph()
  G.add_nodes_from(xrange(n))
  for e in E:
    ee = list(e)
    G.add_edge(ee[0], ee[1])

  paths = []
  for v1 in xrange(n):
    for v2 in xrange(v1 + 1, n):
      for p in nx.all_simple_paths(G, v1, v2, cutoff):
        paths.append(p)
  return paths

def naiveAllPaths1(n, E):
	paths = []
	for v1 in xrange(n):
		for v2 in xrange(v1 + 1, n):
			for path in allSTPaths(n, E, v1, v2):
				paths.append(path)
	return paths

def allSTPaths(n, E, s, t):
	V = set(list(xrange(n)))
	V.remove(s)
	paths = rAllSTPaths(V, E, s, t)
	for path in paths:
		path.append(s)
	return paths

def rAllSTPaths(V, E, s, t):
  toReturn = []
  for v in V:
  	if {s, v} in E: #If we can move from s to the particular v
  		if v == t: #If we arrived at destination, we're good
  			toReturn.append([t])
  		else:
  			#prepare new graph
  			V2 = V.copy()
  			V2.remove(v)
  			paths = rAllSTPaths(V2, E, v, t)
  			for path in paths:
  				path.append(v)
  				toReturn.append(path)
  return toReturn
