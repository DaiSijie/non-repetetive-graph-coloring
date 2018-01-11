## Introduction

Non-repetitive graph coloring is a generalization of regular graph coloring. In this setting, we require all simple path of odd length to be square-free. We say that a sequence is a square if it is of the form xx where x is any sequence of color. We denote by π(G) (Thue number) the minimum number of colors required to produce a proper non-repetitive graph coloring for G.

This repository will contain all the Python code that I'm writting for my semester project at EPFL for the DISOPT lab. It mainly contains small snippets to test hypotheses. Since this problem is very hard (it lies in NP^NP), the problem is translated to an integer program and you will need a working copy of Gurobi (free academic license available!) to execute the code.

You can use it to black-box compute the Thue number/index of any graph (and also retrieve the coloring).

Below you will find a description of each script of interest. When a program requires a graph file, it uses the encoding provided by **EasyGraph** which you can find in one of my other repository. You can find example of graphs in the 'example' folder.

## Computation of π(G)
generalNRGC.py computes the Thue number of any graph and also yields the proper coloring. Note that it may take quite a long time. If you want to color edges (Thue index), append "edge" at the end of the command (or any other string! ;-))

**Usage**: `python generalNRGC.py graphfile (edge)`

**Requirements**: Gurobi

##(Fast) lower bound on π(T(n))
The multigrid of dimension n is a grid of size n x n where every row and column is also a clique of size n (aka rooke graphs). multigridsNRGC.py computes the minimum number of color to provide a proper non-repetitive coloring by only considering paths up to length lim. If you want to consider all paths, put lim = n^2.

**Usage**: `python multigridNRGC.py n lim`

**Requirements**: Gurobi

## Verification of the π(L(T)) - π'(T) ≤ 1 conjecture for some trees
treeNRGC.py test the above conjecture for all trees located in a folder f. The files containing the trees should be the one available on http://users.cecs.anu.edu.au/~bdm/data/trees.html. Script also available in "cluster" mode with log file and recovery options.

**Usage**: `python treeNRGC.py f`

**Requirements**: Gurobi

## Computation of π'(T) and π(T) for complete binary trees
binarytreeNRGC.py computes the Thue number and index of the complete binary tree of level l.

**Usage**: `python binarytreeNRGC.py l`

**Requirements**: Gurobi

## Computation of π(P_n)
pathNRGC.py computes the Thue number of a path of length l and also yields the proper coloring. Note that due to Thue, the number of colors used should always be 3. (There exists also more efficient way to compute those! - see Thue's original paper)

**Usage**: `python pathNRGC.py l`

**Requirements**: Gurobi


## About
Author: Gilbert Maystre

Supervisor: Manuel Aprile
