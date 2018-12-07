"""Provides functions to determine the critical nodes of a graph using different algorithms"""

import networkx as ntx
import operator


def crucialNodesDegree(G, number_of_nodes = 1):
    """ Calculates the nodes with the highest degree betweenness of a graph

    Arguments:
        G -- a networkX graph object
        number_of_nodes -- the length of the returned list
    """

    d = ntx.degree_centrality(G)
    ret = []
    for i in range(0, number_of_nodes-1):
        if d:
            index = max(d.items(), key=operator.itemgetter(1))[0]
            ret.append(index)
            del d[index]
    return ret


def crucialNodesEigenvector(G, number_of_nodes = 1):
    """ Calculates the nodes with the highest eigenvector betweenness of a graph

        Arguments:
            G -- a networkX graph object
            number_of_nodes -- the length of the returned list
        """

    d = ntx.eigenvector_centrality(G)
    ret = []
    for i in range(0, number_of_nodes - 1):
        if d:
            index = max(d.items(), key=operator.itemgetter(1))[0]
            ret.append(index)
            del d[index]
    return ret
