"""Provides functions to plot graphs"""

import networkx as ntx
import matplotlib.pyplot as plt


def plotFromMatrix(A):
    """Plots a graph described by a matrix"""

    graph = ntx.from_numpy_array(A)
    plotFromGraph(graph)


def plotFromGraph(G):
    """Plots a graph described as networkx graph object"""

    plt.figure(plotFromGraph.counter)
    ntx.draw_networkx(G)
    plotFromGraph.counter += 1
