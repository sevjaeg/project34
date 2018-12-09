"""
Run this file to conduct the light reproducibility test

This is Python 3 code (tested under Python 3.7).

The following libraries are required:
    scipy
    networkX
    matplotlib
"""


from centrality import crucialNodesEigenvector
from fetchData import importEdgeListFile
from calculateLambda import obtainMaxEig
from sirFunctions import fig_5_right
from plotGraph import plotFromGraph
import matplotlib
import warnings

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

# Analyzing the first data set #########################################################################################
print("Importing graph")
G = importEdgeListFile('data/terrorist.txt', '\t')
print("Data set TERRORISTS")
print(str(len(G.nodes)) + " nodes")
print("Largest eigenvalue: " + str(round(obtainMaxEig(G), 2)))

critical_nodes = crucialNodesEigenvector(G, number_of_nodes=3)  # Finding the most important nodes in the network
print("Critical nodes: " + str(critical_nodes))

plotFromGraph(G)

print("\n"
      "Removing critical nodes")
for node in critical_nodes:
    G.remove_node(node)

print("Largest eigenvalue: " + str(round(obtainMaxEig(G), 2)))
print("Immunization of critical nodes dramatically reduces the largest eigenvalue")


print("\n"
      "Our model suggests that the largest eigenvalue of the adjacency matrix and a constant belonging to the virus "
      "propagation model"
      "\n"
      "(their product is called effective strength) "
      "determine whether a disease leads to an epidemic or not."
      "\n")

# SIR simulations ######################################################################################################
print("Importing graph")
G = importEdgeListFile("data/as-oregon/as20000102.txt", '\t')
print("Data set AS-OREGON")
print(str(len(G.nodes)) + " nodes")
print("Largest eigenvalue: " + str(round(obtainMaxEig(G), 2)))

# Simulation parameters
initial_size = 10  # initially infected nodes
iterations = 100  # independent calculations for averaging
number_of_steps = 15  # different effective virus strenghts (x-axis values)

print("\n"
      "The following figure shows, that for effective virus strengths below 1 the virus does not spread.")

fig_5_right(G, initial_size, iterations, number_of_steps)  # computation might take one minute

# Challenging model using small networks ###############################################################################

print("\n"
      "Does the model also apply for small networks?")
print("Importing graph")
G = importEdgeListFile('data/terrorist.txt', '\t')
print("Data set TERRORISTS")

initial_size = 3
critical_nodes = crucialNodesEigenvector(G, number_of_nodes=initial_size)

print("\n"
      "Plot: For small networks, the tipping point is below one and the model has reached its limit")
fig_5_right(G, initial_size, iterations, number_of_steps, initial_nodes=critical_nodes)
