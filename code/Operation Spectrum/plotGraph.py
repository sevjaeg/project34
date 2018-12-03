"""Provides functions to plot graphs"""

import networkx as ntx
import matplotlib.pyplot as plt


def plotFromMatrix(A):
    graph = ntx.from_numpy_array(A)
    plotFromGraph(graph)


def plotFromGraph(G):  # TODO: format graphs
    plt.figure(plotFromGraph.counter)
    ntx.draw_networkx(G)
    plotFromGraph.counter += 1


