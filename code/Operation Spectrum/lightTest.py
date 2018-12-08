"""
Run this file to conduct the light reproducibility test

The following libraries are required:
    scipy
    networkX
    matplotlib
"""

from fetchData import importEdgeListFile
from calculateLambda import obtainMaxEig
from sirFunctions import fig_5_right

# TODO: hier ggf. gillespie von Yannick verwenden

print("Importing graph")
G = importEdgeListFile('data/terrorist.txt', '\t')  # TODO: passenden Graph auswählen

print("Largest eigenvalue: " + str(round(obtainMaxEig(G), 3)))

initial_size = 2  # initially infected nodes
iterations = 50  # independent calculations for averaging
number_of_steps = 12  # different effective virus strenghts (x-axis values)

fig_5_right(G, initial_size, iterations, number_of_steps)

# TODO: was mach ma da?
