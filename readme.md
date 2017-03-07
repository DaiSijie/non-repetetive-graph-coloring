This repository contains all the code that I'm writing to test hypotheses for my project on non-repetitive graph coloring.
You will need a working license of Gurobi to run the code

#####
GeneralNRGC.py

Usage: python GeneralNRGC.py graphfile
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

