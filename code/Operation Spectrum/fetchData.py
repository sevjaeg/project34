"""Provides functions to read in graphs from files"""

import numpy as np
import scipy as sp
import networkx as ntx
import sys


def importMatrixFile(path, lineSeparator, columnSeparator):
    """reads a matrix from a file into a nbarray (NO sparse matrix!) and returns the according graph
       file may not be empty (as the first line has to be read)
       each row has to contain the same number of elements (is not checked)
       lines in the file are separated by lineSeparator, columns by columnSeparator"""

    sourceFile = open(path, "r")
    # first line to create a matrix
    line = sourceFile.readline()
    # Excludes special characters from imported string (typical cases considered)
    if line[len(line) - 1] == '\n':
        line = line[:len(line) - 1]
    if line[len(line) - 1] == ' ':
        line = line[:len(line) - 1]
    if line[len(line) - 1] == lineSeparator:
        line = line[:len(line) - 1]
    if line[len(line) - 1] == ' ':
        line = line[:len(line) - 1]
    lineElements = line.split(columnSeparator)
    # Float array to deal with weighted graphs
    try:
        lineElements = [float(i) for i in lineElements]
    except ValueError:
        print("Cannot cast matrix elements to floats!", file=sys.stderr)
        return
    A = np.array(lineElements, dtype=float)
    while True:
        line = sourceFile.readline()
        if line == "" or line == "\n":
            break
        if line[len(line)-1] == '\n':
            line = line[:len(line) -1]
        if line[len(line) - 1] == ' ':
            line = line[:len(line) - 1]
        if line[len(line) - 1] == lineSeparator:
            line = line[:len(line) - 1]
        if line[len(line) - 1] == ' ':
            line = line[:len(line) - 1]
        lineElements = line.split(columnSeparator)
        try:
            lineElements = [float(i) for i in lineElements]
        except ValueError:
            print("Cannot cast matrix elements to floats!", file=sys.stderr)
            return
        # Adds row to existing matrix, assuming same number of elements
        A = np.vstack([A, lineElements])
    sourceFile.close()
    # Converts matrix into networkX graph object
    return ntx.from_numpy_array(A)


def importEdgeListFile(path, elementSeparator):
    """reads a graph from a file containing all edges
       inside a line the two nodes connected by the edge a separated by the elementSeparator"""
    sourceFile = open(path, "r")
    edgelist = []
    while True:
        line = sourceFile.readline()
        if line == '' or line == '\n':
            break
        # Edgelist expects integer values (discrete indices of nodes)
        try:
            edgelist.append(tuple([int(i) for i in line.split(elementSeparator)]))
        except ValueError:
            print("Cannot cast matrix elements to floats!", file=sys.stderr)
            return
    sourceFile.close()
    #Converts edgelist to networkx graph object
    return ntx.from_edgelist(edgelist)


def normalizeGraph(G, threshold):
    """Sets all edge weights of a graph with an absolute value greater than the threshold to 1 and all others to 0"""
    A = ntx.adjacency_matrix(G)
    A = normalizeSparseMatrix(A, threshold)
    return ntx.from_scipy_sparse_matrix(A)


def normalizeMatrix(A, threshold):
    """Sets all values of a matrix with an absolute value greater than the threshold to 1 and all others to 0
    works with ordinary numpy matrices"""
    num = len(A)
    for i in range(0, num):
        for j in range(0, num):
            if np.abs(A[i, j]) > threshold:
                A[i, j] = 1
            else:
                A[i, j] = 0
    return A


def normalizeSparseMatrix(A, threshold):
    """Sets all values of a matrix with an absolute value greater than the threshold to 1 and all others to 0
        works with scipy sparse matrices"""
    positions = A.nonzero()
    for i in range(0, len(positions[0])):
        if A[positions[0][i], positions[1][i]] > threshold:
            A[positions[0][i], positions[1][i]] = 1
        else:
            A[positions[0][i], positions[1][i]] = 0
    return A

