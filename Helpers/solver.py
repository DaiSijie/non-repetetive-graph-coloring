from gurobipy import *

def solve(size, number_of_colors, paths):

  m = Model()

  Y = [] #Y_color
  X = [] #X_color_vertex
  Z = [] #Z_vertex_vertex

  for c in xrange(number_of_colors):
    Y.append(m.addVar(vtype = GRB.BINARY, name = "Y_" + str(c)))
    X_c = []
    for v in xrange(size):
      X_c.append(m.addVar(vtype = GRB.BINARY, name = "X_" + str(c) + "_" + str(v)))
    X.append(X_c)

  for i in xrange(size):
    ins = []
    for j in xrange(size):
      ins.append(0)
    Z.append(ins)

  for v1 in xrange(size):
    Z_v = []
    for v2 in xrange(v1 + 1, size):
      Z[v1][v2] = m.addVar(vtype = GRB.INTEGER, name = "Z_" + str(v1) + "_" + str(v2))

  m.update()

  #First, make sure that every vertex has exactly one color:
  for v in xrange(size):
    constraints = []
    for c in xrange(number_of_colors):
      constraints.append(X[c][v])
    m.addConstr(quicksum(constraints[i] for i in xrange(len(constraints))), GRB.EQUAL, 1, name = str(v) + "_has_exactly_one_color")

  #Then, make sure that every color in activated:
  for c in xrange(number_of_colors):
    for v in xrange(size):
      m.addConstr(X[c][v], GRB.LESS_EQUAL, Y[c], name = "color_" + str(v) + "_is_activated_wrpt_" + str(v))

  #Constraints the Z:
  for v1 in xrange(size):
    for v2 in xrange(v1 + 1, size):
      for c in xrange(number_of_colors):
        m.addConstr(X[c][v1] + X[c][v2], GRB.LESS_EQUAL, Z[v1][v2], name = "z_max_for_" + str(v1) + "_" + str(v2))
      m.addConstr(Z[v1][v2], GRB.LESS_EQUAL, 2, name = "z_ok"+str(v1)+str(v2))

  #Now, constraint every path:
  for path in paths:
    length = len(path)
    constraints = []
    for i in xrange(length/2):
      constraints.append(getZFor(Z, path[i], path[i + length/2]))
    m.addConstr(quicksum(constraints[i] for i in xrange(len(constraints))), GRB.LESS_EQUAL, length - 1, name = "path_" + str(path) + "_ok")

  m.update()

  m.setObjective(quicksum(y for y in Y), GRB.MINIMIZE)
  m.optimize()

  return parseSolution(Y, X)

def getZFor(Z, v1, v2):
  return Z[min(v1, v2)][max(v1,v2)]

def parseSolution(Y, X):
  nOfColors = 0
  for y in Y:
    nOfColors += y.X

  assignment = [] #at position i lies the color vertex i must take
  for v in xrange(len(X)):
    for c in xrange(len(X)):
      if X[c][v].X > 0.0:
        assignment.append(c)

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

  return (int(nOfColors), assignment)
