"""Provides functions for calculation of the largest eigenvalue of a graph"""

import numpy as np
import scipy as sp
import networkx as ntx
import sys


def maxEig(A):
    """Returns the largest eigenvalue (absolute value) of a symmetric matrix

    Arguments:
        A -- a real symmetric N x N matrix
    """
    eigenVals = sp.sparse.linalg.eigsh(sp.sparse.csr_matrix.asfptype(A), k=1, return_eigenvectors=False, which='LM')
    return abs(eigenVals[0])


def obtainMaxEig(G, out=False, digits=0):
    """Returns the largest eigenvalue (absolute value) of the adjacency matrix belonging to a graph

    Arguments:
        G -- a networkX graph object
        out -- when True, the eigenvalue is printed to the console (default False)
        digits -- the rounding accuracy of the printed eigenvalue (default 0)
    """

    A = ntx.adjacency_matrix(G)
    try:
        ret = maxEig(A)
    except np.linalg.LinAlgError:
        print("Cannot calculate eigenvalues!", file=sys.stderr)
        return 0
    if out:
        print(np.round(ret, digits))
    return ret

