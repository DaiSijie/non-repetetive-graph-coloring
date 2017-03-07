import Paths
import Solver

def construct(n):
  E = set()

  nvertices = n * n
  for i in xrange(n):
    for j in xrange(n):
      for k in xrange(j+1, n):
        E.add(frozenset([n * i + j, n * i + k]))

  for j in xrange(n):
    for i in xrange(n):
      for k in xrange(i + 1, n):
        E.add(frozenset([i * n + j, k * n + j]))

  return E


if __name__ == '__main__':
  

  print "l = "+str(len(construct(4)))


  E = construct(4)
  (colors, assignment) = Solver.solve(16, 16, Paths.allPaths(16, E))
  print "n of colors: "+str(colors)


  #for i in xrange(6):
   #E = construct(i)
    #(colors, assignment) = Solver.solve(i * i, i * i, Paths.allPaths(i * i, E))
    #print "size of E: " + str(len(E))
    #print "n of colors: " + str(colors)
