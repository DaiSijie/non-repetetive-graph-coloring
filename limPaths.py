import sys

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
  if len(sys.argv) < 3:
    print "Usage: \"python GeneralNRGC.py graphFile\""
  else:
    f = open(sys.argv[1])
    lim = int(sys.argv[2])
    (size, E, forwardMap, backwardMap) = fromEasyGraphFlow(f.read())
    paths = allPaths(size, E, lim)
    print "numbers: "+str(len(paths))
    print paths