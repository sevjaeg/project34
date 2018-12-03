"""Provides functions to determine the critical nodes of a graph using different algorithms"""

import networkx as ntx
import operator

def crucialNodesDegree(G, number_of_nodes = 1):  # very simple degree depending on the number of edges connected to a node
    d = ntx.degree_centrality(G)
    ret = []
    for i in range(0, number_of_nodes-1):
        if d:
            index = max(d.items(), key=operator.itemgetter(1))[0]
            ret.append(index)
            del d[index]
    return ret

def crucialNodesBetweenness(G, number_of_nodes = 1):  # expensive computation, degree depending on the paths going through the node
    d = ntx.betweenness_centrality(G)
    ret = []
    for i in range(0, number_of_nodes - 1):
        if d:
            index = max(d.items(), key=operator.itemgetter(1))[0]
            ret.append(index)
            del d[index]
    return ret


def crucialNodesEigenvector(G, number_of_nodes = 1):  # modest performance, degree based on adjacency matrix eigenvalues
    d = ntx.eigenvector_centrality(G)
    ret = []
    for i in range(0, number_of_nodes - 1):
        if d:
            index = max(d.items(), key=operator.itemgetter(1))[0]
            ret.append(index)
            del d[index]
    return ret
