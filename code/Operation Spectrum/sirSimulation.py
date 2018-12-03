"""Reproduction of the original paper using the Gillespie algorithm for SIR simulation"""

from sirFunctions import fig_5_left, fig_5_right, fig_5_right_initial
from fetchData import importEdgeListFile
from calculateLambda import obtainMaxEig

# Data source (similar to AS-Oregon used in the original paper)
E = importEdgeListFile("data/as-oregon/as20000102.txt", '\t')
#E = importEdgeListFile("data/as-oregon/as20010331.txt", ':')
#E = importEdgeListFile("data/facebook_combined.txt", ' ')

# Simulation parameters
initial_size = 1000  # number of initially infected nodes (randomly distributed) for fig_5_left and fig_5_right
initial_sizes = [2, 10, 25, 100]  # different initial sizes for fig_5_right_initial
iterations = 10  # number of independent simulation runs (overall results are average) for all three functions
number_of_steps = 20  # number of different s-values in fig_5_right and fig_5_right_initial


eig = obtainMaxEig(E, False, 2)
print(str(len(E.nodes)) + " nodes")
print("Largest Eigenvalue of the adjacency matrix = " + str(round(eig, 2)))


# Figures from the original paper (page 13) for reproduction
fig_5_left(E, initial_size, 20*iterations)
fig_5_right(E, initial_size, iterations, number_of_steps)

# Plot
fig_5_right_initial(E, initial_sizes, iterations, number_of_steps)
