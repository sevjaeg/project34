"""Reproduction of the original paper using the Gillespie algorithm for SIR simulation"""

from sirFunctions import fig_5_left, fig_5_right, fig_5_right_initial
from fetchData import importEdgeListFile
from calculateLambda import obtainMaxEig
from centrality import crucialNodesEigenvector


# Data source (for details see data/readme.md) #########################################################################

E = importEdgeListFile("data/as-oregon/as20000102.txt", '\t')
#E = importEdgeListFile("data/as-oregon/as20010331.txt", ':')
#E = importEdgeListFile("data/facebook_ego.txt", ' ')
#E = importEdgeListFile('data/terrorist.txt', '\t')


# Simulation parameters ################################################################################################

initial_size = 10  # number of initially infected nodes
initial_sizes = [2, 20, 80, 160]  # different initial sizes for fig_5_right_initial
iterations = 50  # number of independent simulation runs (overall results are average) for all three functions
number_of_steps = 40  # number of different s-values in fig_5_right and fig_5_right_initial

eig = obtainMaxEig(E)
print(str(len(E.nodes)) + " nodes")
print("Largest Eigenvalue of the Adjacency Matrix = " + str(round(eig, 2)))


# Figures from the original paper (page 13) for reproduction (random infected nodes) ###################################

#fig_5_left(E, initial_size, 20*iterations)
#fig_5_right(E, initial_size, iterations, number_of_steps, parallel=True)
#fig_5_right_initial(E, initial_sizes, iterations, number_of_steps, parallel=True)  # different sizes of initial infection


# Same figures, critial nodes infected #################################################################################

# initializing crucial nodes
initial_nodes = crucialNodesEigenvector(E, number_of_nodes=initial_size)
initial_nodes_array = list()
for i in range(0, len(initial_sizes)):
    initial_nodes_array.append(crucialNodesEigenvector(E, number_of_nodes=initial_sizes[i]))

#fig_5_left(E, len(initial_nodes)+1, 20*iterations, initial_nodes=initial_nodes)
fig_5_right(E, len(initial_nodes)+1, iterations, number_of_steps, initial_nodes=initial_nodes, parallel=True)
#fig_5_right_initial(E, initial_sizes, iterations, number_of_steps, initial_nodes=initial_nodes_array, parallel=True)  # different sizes of initial infection
