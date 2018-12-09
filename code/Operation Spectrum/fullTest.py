"""
Reproduction of our work

Note that the term 'paper' in this section refers to B. Aditya Prakash, D. Chakrabarti, N. Valler, M. Faloutsos, C. Faloutsos (2012):
Threshold Conditions for Arbitrary Cascade Models on Arbitrary Networks. Knowledge and Information Systems manuscript No. KAIS-12-3483R
"""

from sirFunctions import fig_5_left, fig_5_right, fig_5_right_initial
from fetchData import importEdgeListFile
from calculateLambda import obtainMaxEig
from centrality import crucialNodesEigenvector


# Data sources (for details see data/readme.md) ########################################################################

E = importEdgeListFile("data/as-oregon/as20000102.txt", '\t') # used for reproduction of the paper
#E = importEdgeListFile("data/facebook_ego.txt", ' ')  # used for validation of the paper
#E = importEdgeListFile('data/terrorist.txt', '\t')  # used to challenge the model with a small network


# Simulation parameters ################################################################################################

initial_size = 0  # number of initially infected nodes
initial_sizes = []  # different initial sizes for fig_5_right_initial
iterations = 0  # number of independent simulation runs (overall results are average) for all three functions
number_of_steps = 0  # number of different s-values in fig_5_right and fig_5_right_initial


# Reproduction of SIR figures from the paper (page 13) #################################################################

initial_size = 10
iterations = 200  # strongly affects computation effort (200 used for report)
number_of_steps = 20

print("Data set AS-OREGON")
eig = obtainMaxEig(E)
print(str(len(E.nodes)) + " nodes")
print("Largest Eigenvalue of the Adjacency Matrix = " + str(round(eig, 2)))

beta = [0.1/eig, 0.5/eig, 20/eig, 100/eig]  # Defining the different s values (as s = eig*beta/delta)
delta = [1, 1, 1, 1]

fig_5_left(E, initial_size, 10*iterations, beta=beta, delta=delta)
fig_5_right(E, initial_size, iterations, number_of_steps)


# Investigating the influence of the number of initial nodes ###########################################################

initial_sizes = [10, 100, 1000]
fig_5_right_initial(E, initial_sizes, iterations, number_of_steps)


# Investigating the influence of infecting the nodes with the highest eigenvector centrality ###########################

initial_nodes = crucialNodesEigenvector(E, number_of_nodes=initial_size)
print("Nodes with highest betweenness: " + str(initial_nodes))

fig_5_right(E, initial_size, iterations, number_of_steps, show=False)
fig_5_right(E, initial_size, iterations, number_of_steps, initial_nodes=initial_nodes)

initial_nodes_array = list()
for i in range(0, len(initial_sizes)):
    initial_nodes_array.append(crucialNodesEigenvector(E, number_of_nodes=initial_sizes[i]))


# Combining infection of critical nodes with different number of initial nodes #########################################

fig_5_right_initial(E, initial_sizes, iterations, number_of_steps, initial_nodes=initial_nodes_array)


# Time behaviour when nodes with highest centrality are infected #######################################################

beta = [0.5/eig, 0.8/eig, 3/eig, 10/eig]
fig_5_left(E, initial_size, 10*iterations, initial_nodes=initial_nodes, beta=beta, delta=delta)


# Validation of the paper using a different graph ######################################################################

print("Data set FACEBOOK-EGO")
E = importEdgeListFile("data/facebook_ego.txt", ' ')

eig = obtainMaxEig(E)
print("\n" + str(len(E.nodes)) + " nodes")
print("Largest Eigenvalue of the Adjacency Matrix = " + str(round(eig, 2)))

initial_nodes = crucialNodesEigenvector(E, number_of_nodes=initial_size)
print("Nodes with highest betweenness: " + str(initial_nodes))


fig_5_right(E, initial_size, iterations, number_of_steps, show=False)
fig_5_right(E, initial_size, iterations, number_of_steps, initial_nodes=initial_nodes)

initial_nodes_array = list()
for i in range(0, len(initial_sizes)):
    initial_nodes_array.append(crucialNodesEigenvector(E, number_of_nodes=initial_sizes[i]))

fig_5_right_initial(E, initial_sizes, iterations, number_of_steps, initial_nodes=initial_nodes_array)


# Challenging the model using a small network ##########################################################################

print("Data set TERRORISTS")
E = importEdgeListFile('data/terrorist.txt', '\t')

eig = obtainMaxEig(E)
print("\n" + str(len(E.nodes)) + " nodes")
print("Largest Eigenvalue of the Adjacency Matrix = " + str(round(eig, 2)))

initial_sizes = [1, 2, 5]

initial_nodes_array = list()
for i in range(0, len(initial_sizes)):
    initial_nodes_array.append(crucialNodesEigenvector(E, number_of_nodes=initial_sizes[i]))

fig_5_right_initial(E, initial_sizes, 5*iterations, number_of_steps, initial_nodes=initial_nodes_array)
