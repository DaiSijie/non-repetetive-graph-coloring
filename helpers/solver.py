from gurobipy import *

def solveForEdges(E, number_of_colors, paths):
  #Apply conversion
  (size, fwdmap, bckmap) = conversion(E)
  paths = filter(lambda path: len(path) % 2 == 1 and len(path) > 1, paths)
  paths = map(lambda path: translate(path, fwdmap), paths)

  #Actually solve it
  (feasible, nOfColors, assignment) = solve(size, number_of_colors, paths)

  if not feasible:
    return (False, 0, [])
  else:
    ass = []
    for i in xrange(size):
      ass.append((bckmap[i], assignment[i]))
    return (True, nOfColors, ass)

def conversion(E):
  counter = 0
  fwdmap = dict()
  bckmap = dict()
  for e in E:
    l = list(e)
    a = max(l[0], l[1])
    b = min(l[0], l[1])
    fwdmap[(a, b)] = counter
    bckmap[counter] = (a, b)
    counter = counter + 1
  return (counter, fwdmap, bckmap)

def translate(path, fwdmap):
  l = len(path)
  for i in xrange(l-1):
    a = max(path[i], path[i + 1])
    b = min(path[i], path[i + 1])
    path[i] = fwdmap[(a, b)]
  del path[l-1]
  return path

def solve(size, number_of_colors, paths):
  m = Model()

  m.setParam( 'OutputFlag', False )

  Y = [] #Y_color
  X = [] #X_color_vertex
  Z = [] #Z_vertex_vertex

  for c in xrange(number_of_colors):
    Y.append(m.addVar(vtype = GRB.BINARY))
    X_c = []
    for v in xrange(size):
      X_c.append(m.addVar(vtype = GRB.BINARY))
    X.append(X_c)

  for i in xrange(size):
    ins = []
    for j in xrange(size):
      ins.append(0)
    Z.append(ins)

  for v1 in xrange(size):
    Z_v = []
    for v2 in xrange(v1 + 1, size):
      Z[v1][v2] = m.addVar(vtype = GRB.INTEGER)

  m.update()

  #First, make sure that every vertex has exactly one color:
  for v in xrange(size):
    constraints = []
    for c in xrange(number_of_colors):
      constraints.append(X[c][v])
    m.addConstr(quicksum(constraints[i] for i in xrange(len(constraints))), GRB.EQUAL, 1)

  #Then, make sure that every color in activated:
  for c in xrange(number_of_colors):
    for v in xrange(size):
      m.addConstr(X[c][v], GRB.LESS_EQUAL, Y[c])

  #Constraints the Z:
  for v1 in xrange(size):
    for v2 in xrange(v1 + 1, size):
      for c in xrange(number_of_colors):
        m.addConstr(X[c][v1] + X[c][v2], GRB.LESS_EQUAL, Z[v1][v2])
      m.addConstr(Z[v1][v2], GRB.LESS_EQUAL, 2)

  #Now, constraint every path:
  for path in paths:
    length = len(path)
    constraints = []
    for i in xrange(length/2):
      constraints.append(getZFor(Z, path[i], path[i + length/2]))
    m.addConstr(quicksum(constraints[i] for i in xrange(len(constraints))), GRB.LESS_EQUAL, length - 1)

  m.update()

  m.setObjective(quicksum(y for y in Y), GRB.MINIMIZE)
  m.optimize()

  if m.status == GRB.Status.INFEASIBLE:
    return (False, 0, [])
  else:
    return parseSolution(Y, X)

def getZFor(Z, v1, v2):
  return Z[min(v1, v2)][max(v1,v2)]

def parseSolution(Y, X):
  nOfColors = 0
  for y in Y:
    nOfColors += y.X

  assignment = [0]*len(X[0]) #at position i lies the color vertex i must take
  for c in xrange(len(X)):
    for v in xrange(len(X[c])):
      if X[c][v].X > 0.0:
        assignment[v] = c

  #Now we rename colors in a two-pass fashion
  C = set()
  for c in assignment:
    C.add(c)

  renaming = dict()
  counter = 0
  for c in C:
    renaming[c] = counter
    counter = counter + 1

  assignment = map(lambda x: renaming[x], assignment)

  return (True, int(nOfColors), assignment)

