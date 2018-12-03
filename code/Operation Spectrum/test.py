"""Provides testing capabilities for the graph-related functions"""

import warnings
import matplotlib.cbook
import matplotlib.pyplot as plt

from plotGraph import plotFromGraph
from fetchData import importMatrixFile, importEdgeListFile, normalizeGraph
from calculateLambda import obtainMaxEig, removeCriticalNode
from centrality import crucialNodesEigenvector, crucialNodesBetweenness, crucialNodesDegree

# suppresses warning while creating plot
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

# initializes the plot counter to show multiple plot windows
plotFromGraph.counter = 1


# Data source (for details see data/readme.md) #########################################################################

G = importEdgeListFile('data/terrorist.txt', '\t')
#G = importEdgeListFile("data/facebook_ego.txt", ' ')
#G = importEdgeListFile("data/as-oregon/as20000102.txt", '\t')  # Warning: Too large to plot or immunize
#G = importEdgeListFile("data/as-oregon/as20010331.txt", ':')  # Warning: Too large to plot or immunize


# Eigenvalue compuatation ##############################################################################################

#print("Larges eigenvalue:")
obtainMaxEig(G, out=True, digits=5)
#plotFromGraph(G)


# Immunization #########################################################################################################

#print("Largest eigenvalue after immunization")
print(crucialNodesEigenvector(G))
print(crucialNodesDegree(G))
#print(crucialNodesBetweenness(G))
G.remove_node(crucialNodesEigenvector(G))
#obtainMaxEig(G, True, 3)
#plotFromGraph(G)


# necessary to avoid blocking of the script execution, plots are displayed when script is done
plt.show()
