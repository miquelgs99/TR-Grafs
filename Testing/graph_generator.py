import networkx as nx
import numpy as np


def grafo(*args):
    size = 10
    matrix = np.random.randint(2, size=(size, size))

    for i in range(len(matrix)):
        matrix[i][i] = 0
    G = nx.from_numpy_matrix(matrix)

    nx.draw_random(G)

