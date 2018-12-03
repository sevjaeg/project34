"""Provides functions for calculation of the largest eigenvalue of a graph"""

import copy
import numpy as np
import scipy as sp
import networkx as ntx
import sys


def maxEig(A):
    """Returns the largest eigenvalue (absolute value) of a symmetric matrix"""
    eigenVals = sp.sparse.linalg.eigsh(sp.sparse.csr_matrix.asfptype(A), k=1, return_eigenvectors=False, which='LM')
    return abs(eigenVals[0])


def obtainMaxEig(G, out, digits):
    """Returns the largest eigenvalue (absolute value) of the adjacency matrix belonging to the graph G
       if out is True, the result of maxEig is printed with precision digits"""
    A = ntx.adjacency_matrix(G)
    try:
        ret = maxEig(A)
    except np.linalg.LinAlgError:
        print("Cannot calculate eigenvalues!", file=sys.stderr)
        return 0
    if out:
        print(np.round(ret, digits))
    return ret


def removeCriticalNode(G):  # poor performance due to some workarounds
    ret = copy.deepcopy(G)
    """Finds the node, which contributes to the largest eigenvalue the most, an deletes is from G. Therefore,
        the returned graph has the lowest possible largest eigenvalue after removing one node."""
    nodeToRemove = 1
    minEig = obtainMaxEig(G, False, 0)
    # WARNING: The index starts at 0, because in edgelists the first node tends to have the index 1. Nevertheless, some graphs might
    # also have a node 0, which is NOT CONSIDERED in this function!
    # Additionally, missing nodes will cause problems with this function
    for i in range(1, len(G.nodes)):
        newG = copy.deepcopy(G)
        newG.remove_node(i)
        currentEig = obtainMaxEig(newG, False, 0)
        if(currentEig == 0):
            print("Eigenvalue computation for node " + str(i) + " not successful!", file=sys.stderr)
        if(currentEig < minEig):
            nodeToRemove = i
            minEig = currentEig
    ret.remove_node(nodeToRemove)
    print("removed node: " + str(nodeToRemove))
    # Workaround to enable multiple vaccination
    matrix = ntx.adj_matrix(ret)
    ret = ntx.from_scipy_sparse_matrix(matrix)
    return ret
