"""Provides testing capabilities for the graph-related functions"""

# TODO: löschen, wenn sonst alles fertig

import warnings
import matplotlib.cbook
import matplotlib.pyplot as plt

from plotGraph import plotFromGraph
from fetchData import importEdgeListFile
from calculateLambda import obtainMaxEig
from centrality import crucialNodesEigenvector, crucialNodesDegree


# suppresses warning while creating plot
from sirFunctions import fig_5_left

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

# initializes the plot counter to show multiple plot windows
plotFromGraph.counter = 1


# Data source (for details see data/readme.md) #########################################################################

#G = importEdgeListFile('data/terrorist.txt', '\t')
#G = importEdgeListFile("data/facebook_ego.txt", ' ')
G = importEdgeListFile("data/as-oregon/as20000102.txt", '\t')  # Warning: Too large to plot
#G = importEdgeListFile("data/as-oregon/as20010331.txt", ':')  # Warning: Too large to plot


# Testing on different beta and delta values

initial_size = 10
iterations = 50  # strongly affects computation effort (200 used for report)
number_of_steps = 20

eig = obtainMaxEig(G)
print("Largest Eigenvalue of the Adjacency Matrix = " + str(round(eig, 2)))

delta = [0.01, 0.01, 10, 10]
beta = [0.5/eig*delta[0], 5/eig*delta[1], 0.5/eig*delta[2], 5/eig*delta[3]]  # Defining the different s values (as s = eig*beta/delta)

fig_5_left(G, initial_size, 10*iterations, beta=beta, delta=delta)  # more iterations possible due to better performance




# Eigenvalue compuatation ##############################################################################################

#print("Larges eigenvalue:")
#obtainMaxEig(G, out=True, digits=5)
#plotFromGraph(G)


# Immunization #########################################################################################################

#print("Largest eigenvalue after immunization")
#print(crucialNodesEigenvector(G))
#print(crucialNodesDegree(G))
#print(crucialNodesBetweenness(G))
#G.remove_node(crucialNodesEigenvector(G))
#obtainMaxEig(G, True, 3)
#plotFromGraph(G)


# necessary to avoid blocking of the script execution, plots are displayed when script is done
plt.show()
