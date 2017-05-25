import random

def findMaximalClique(n, E, iterations = 1):
	#create hashlist representation
	neighbors = [set() for _ in range(n)]
	for e in E:
		(a, b) = (list(e)[0], list(e)[1])
		neighbors[a].add(b)
		neighbors[b].add(a)

	#heuristic: find the vertex with largest degree, and try to grow on it.
	maxi = -1
	maxv = -1 
	for i in xrange(n):
		if len(neighbors[i]) > maxv:
			maxv = len(neighbors[i])
			maxi = i

	#Now retry a few times, with initial guess biggest degree vertex.
	best = set()
	nextv = maxv
	for i in xrange(iterations):
		clique = growGreedily(n, neighbors, nextv)
		if len(clique) > len(best):
			best = clique
		nextv = random.randint(0, n-1)

	return best


def growGreedily(n, neighbors, start):
	clique = set()
	clique.add(start)
	for v in xrange(n):
		if v != start and neighbors[v].issubset(clique):
			clique.add(v)
	return clique