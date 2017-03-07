import sys
import Solver

def displayResults(n, assignment):
  print "\n========== RESULTS =========="
  
  print "Number of colors used: " + str(int(n))
  
  for v in xrange(len(assignment)):
    print "Vertex "+str(v)+": "+str(assignment[v])

  print "============================="

def generatePaths(size):
  paths = []
  for length in xrange(2, size + 1, 2): #All even-length in range 2..size
    for start in xrange(0, size - length + 1):
      p = []
      for v in xrange(length):
        p.append(v + start)
      paths.append(p)
  return paths

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: \"python NRGC.py sizeOfPath\""
  else:
    size = int(sys.argv[1])
    displayResults(*Solver.solve(size, size, generatePaths(size)))
