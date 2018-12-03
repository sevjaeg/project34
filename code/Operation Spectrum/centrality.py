"""TODO: dok"""

import networkx as ntx
import numpy as np
import operator

def crucialNodeDegree(G):  # very simple degree depending on the number of edges connected to a node
    d = ntx.degree_centrality(G)
    return max(d.items(), key=operator.itemgetter(1))[0]


def crucialNodeBetweenness(G):  # expensive computation, degree depending on the paths going through the node
    d = ntx.betweenness_centrality(G)
    return max(d.items(), key=operator.itemgetter(1))[0]


def crucialNodeEigenvector(G):
    d = ntx.eigenvector_centrality(G)
    return max(d.items(), key=operator.itemgetter(1))[0]
