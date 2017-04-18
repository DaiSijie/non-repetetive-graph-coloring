from collections import deque
import copy

class SeparatePathsFinder():
	
	def __init__(self, n, E):
		self.n = n
		self.E = E
		self.trivialPathsGiven = False
		self.queue = deque()
		self.neighbors = [set() for _ in xrange(n)]
		
		for e in self.E:
			(a, b) = (list(e)[0], list(e)[1])
			self.neighbors[a].add(b)
			self.neighbors[b].add(a)

	def __start__(self):
		toReturn = list()
		for e in self.E:
			(a, b) = (list(e)[0], list(e)[1])
			new = deque([a, b])
			toReturn.append(new)
			self.queue.append(new)
		return toReturn

	def popEverything(self):
		toReturn = list()
		c = self.next()
		while len(c) > 0:
			toReturn.extend(c)
			c = self.next()
		return toReturn

	def next(self):
		if not self.trivialPathsGiven:
			self.trivialPathsGiven = True
			return self.__start__()
		if len(self.queue) == 0:
			return list()
		
		#Will not work on longer paths!
		target = len(self.queue[0])
		toReturn = list()

		leftNeighbors = list()
		rightNeighbors = list()
		while len(self.queue) > 0 and len(self.queue[len(self.queue) -1 ]) == target:
			current = self.queue.pop()
			l = len(current)
			left = current[0]
			right = current[l - 1]

			#find all doable neighbors
			rightNeighbors = filter(lambda b: self.okToAddRight(b, current), self.neighbors[right])
			leftNeighbors = filter(lambda a: self.okToAddLeft(a, current), self.neighbors[left])

			#Now, try everything!
			for a in leftNeighbors:
				for b in rightNeighbors:
					if not a == b:
						new = copy.copy(current)
						new.appendleft(a)
						new.append(b)
						toReturn.append(new)
						if a not in self.neighbors[b]: #Goes to next stage
							self.queue.appendleft(new)

			del leftNeighbors[:]
			del rightNeighbors[:]

		return toReturn

	def okToAddLeft(self, a, path):
		l = len(path)/2
		for i in xrange(2*l):
			if a == path[i] or (i >= l and a in self.neighbors[path[i]]):
				return False
		return True

	def okToAddRight(self, a, path):
		l = len(path)/2
		for i in xrange(2*l):
			if a == path[i] or (i < l and a in self.neighbors[path[i]]):
				return False
		return True
		