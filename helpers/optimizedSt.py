import Queue


def allSTPaths(V, E, s, t, S = list()):
	print "called with s = " + str(s) + " t = " + str(t)
	if s == t:
		print "yay!!"
		print S

	r = -1
	for e in E:
		if s in e:
			ee = list(e)
			r = ee[1] if ee[0] == s else ee[0]
			break
	
	if r == -1:
		return
	e = frozenset(list([s, r]))
	print "chosen arc: " + str(e)

	V.remove(s)
	saved = filter(lambda x: s in x, list(E))
	E = set(filter(lambda x: s not in x, E))
	exists = existsPath(V, E, r, t)
	E.update(saved)
	V.add(s)

	if not exists:
		E.remove(e)
		allSTPaths(V, E, s, t, S)
		E.add(e)
		return

	E.remove(e)
	exists = existsPath(V, E, s, t)
	E.add(e)
	
	if not exists:
		E.remove(e)
		Sp = list(S)
		Sp.append(s)
		allSTPaths(V, E, r, t, Sp)
		E.add(e)
		return

	V.remove(s)
	saved = filter(lambda x: s in x, list(E))
	E = set(filter(lambda x: s not in x, E))
	allSTPaths(V, E, r, t, S)
	E.update(saved)
	V.add(s)

	E.remove(e)
	allSTPaths(V, E, s, t, S)
	E.add(s)

	return


def existsPath(V, E, s, t):
	queue = Queue.Queue()
	queue.put(s)
	visited = set()
	while not queue.empty():
		visiting = queue.get()
		visited.add(visiting)
		for e in E:
			if visiting in e:
				ee = list(e)
				other = ee[1] if ee[0] == visiting else ee[0]
				if other not in visited:
					if other == t:
						return True
					queue.put(other)
	return False

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
	dim = 3
	E = buildMultigrid(dim)
	V = set(xrange(dim * dim))
	paths = allSTPaths(V, E, 0, dim * dim - 1)

