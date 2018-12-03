"""Provides testing capabilities for the graph-related functions """

import warnings
import matplotlib.cbook
import matplotlib.pyplot as plot
import networkx as ntx
import numpy as np

from plotGraph import plotFromGraph
from fetchData import importMatrixFile, importEdgeListFile, normalizeGraph
from calculateLambda import obtainMaxEig, removeCriticalNode
from centrality import crucialNodeEigenvector, crucialNodeBetweenness, crucialNodeDegree

# suppresses warning while creating plot
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

# initializes the plot counter to show multiple plot windows
plotFromGraph.counter = 1

# Select data set (for information on the data sets consider data/readme.md)
#G = importMatrixFile(".\data\windsurfers.txt", '\n', ' ')
#G = importMatrixFile(".\data\guineaTribe.txt", '\n', ' ')
#G = importMatrixFile(".\data\windsurfers.txt", '\n', ' ')  # only weighted graph, use normalizeGraph
#G = importEdgeListFile('data/terrorist.txt', '\t')
#G = importEdgeListFile("data/facebook_combined.txt", ' ')
#G = importEdgeListFile("data/as-oregon/as20000102.txt", '\t')  # Warning: Too large to plot or immunize
G = importEdgeListFile("data/as-oregon/as20010331.txt", ':')  # Warning: Too large to plot or immunize
#G = importEdgeListFile(".\data\hyves\edges.csv", ',')  # Warning: Too large to normalize, immunize or plot

#G = normalizeGraph(G, 0.35)

# Eigenvalue compuatation
#print("Larges eigenvalue:")
obtainMaxEig(G, True, 5)
#plotFromGraph(G)

# Immunization
#print("Largest eigenvalue after immunization")
#G1 = removeCriticalNode(G)
#obtainMaxEig(G1, True, 3)
#plotFromGraph(G1)

# Searching critical node
print(crucialNodeEigenvector(G))
print(crucialNodeDegree(G))
#print(crucialNodeBetweenness(G))

G.remove_node(crucialNodeEigenvector(G))
obtainMaxEig(G, True, 5)

# necessary to avoid blocking of the script execution, plots are displayed when script is done
plot.show()
