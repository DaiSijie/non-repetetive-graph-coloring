##Introduction

Non-repetitive graph coloring is a generalization of regular graph coloring. In this setting, we require all simple path of even length to be square-free. We say that a sequence is a square if it is of the form xx where x is any sequence of color. We denote by π(G) (Thue number) the minimum number of colors required to produce a proper non-repetitive graph coloring for G.

This repository will contain all the Python code that I'm writting for my semester project at EPFL for the DISOPT lab. It mainly contains small snippets to test hypotheses. Since this problem is very hard (it lies in CO-NP), the problem is translated to an integer program and you will need a working copy of Gurobi (an L/IP solver) to execute the code.

Below you will find a description of each executable piece of code. When a program requires a graph file, it uses the encoding provided by **EasyGraph** which you can find in one of my other repository.

##Computation of π(G)
generalNRGC.py computes the Thue number of any graph and also yields the proper coloring. Note that it may take quite a long time.

**Usage**: `python generalNRGC.py graphfile`

**Requirements**: Gurobi, Networkx

##Fast lower bound on π(T(n))
The multigrid of dimension n is a grid of size n x n where every row and column is also a clique of size n. multigridsNRGC.py computes the minimum number of color to provide a proper non-repetitive coloring by only considering paths up to length lim. If you want to consider all paths, put lim = n^2.

**Usage**: `python multigridNRGC.py n lim`

**Requirements**: Networkx, Gurobi

##Verification of the π(L(T)) ≤ π'(T) conjecture for some trees
treeNRGC.py test the above conjecture for all trees located in a folder f. The files containing the trees should be the one available on http://users.cecs.anu.edu.au/~bdm/data/trees.html

**Usage**: `python treeNRGC.py f`

**Requirements**: Gurobi, Networkx


##Computation of π(P_n)
pathNRGC.py computes the Thue number of a path of length l and also yields the proper coloring. Note that due to Thue, the number of colors used should always be 3.

**Usage**: `python pathNRGC.py l`

**Requirements**: Gurobi


##About
Author: Gilbert Maystre

Supervisor: Manuel Aprile
