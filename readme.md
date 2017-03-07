#Introduction

Non-repetitive graph coloring is a generalization of regular graph coloring. In this setting, we require all simple path of even length to be square-free. We say that a sequence is a square if it is of the form xx where x is any sequence of color. We denote by π(G) (Thue number) the minimum number of colors required to produce a proper non-repetitive graph coloring for G.

This repository will contain all the Python code that I'm writting for my semester project at EPFL for the DISOPT lab. It mainly contains small snippets to test hypotheses. Since this problem is very hard (it lies in CO-NP), the problem is translated to an integer program and you will need a working copy of Gurobi (an L/IP solver) to execute the code.

Below you will find a description of each executable piece of code which. When a program requires a graph file, it uses the encoding provided by **EasyGraph** which you can find in one of my other repository.


##GeneralNRGC.py
**Usage**: python GeneralNRGC.py graphfile
**Requirements**: Gurobi, networkx

Requires networkx

####
PathNRGC.py

Usage: python PathNRGC.py l
Where l is the length of the path

####
multigrids

Usage: python multigrids.py n lim
We define a multigrid as the grid of size n x n where every row and column is a clique of size n. lim represents the maximal size of paths considered. Putting a small lim will make the programm run faster but will only provide a lower bound on pi(M_4).

####

