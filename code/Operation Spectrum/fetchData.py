"""Provides functions to read in graphs from files"""

import numpy as np
import networkx as ntx
import sys


def importMatrixFile(path, rowSeparator, columnSeparator):
    """Reads an adjacency matrix file and returns the respective graph

    Arguments:
        path -- path of a non-empty file containing an adjacency matrix
        rowSeparator -- character seperating two rows of the matrix in the file
        columnSeparator -- character seperating two columns of the matrix in the file
    """

    sourceFile = open(path, "r")
    # first line to create a matrix
    line = sourceFile.readline()
    # Excludes special characters from imported string (typical cases considered)
    if line[len(line) - 1] == '\n':
        line = line[:len(line) - 1]
    if line[len(line) - 1] == ' ':
        line = line[:len(line) - 1]
    if line[len(line) - 1] == rowSeparator:
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
        if line[len(line) - 1] == rowSeparator:
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
    """Reads an edge list file and returns the respective graph

    Arguments:
        path -- path of a non-empty file containing an edge list
        elementSeparator -- character seperating the two connected nodes in the edgelist (lines separated by '\n' by default)
    """

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
            print("Cannot cast matrix elements to integers!", file=sys.stderr)
            return
    sourceFile.close()
    #Converts edgelist to networkx graph object
    return ntx.from_edgelist(edgelist)
