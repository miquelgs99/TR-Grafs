import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def grafo(*args):
    size = 10
    matrix = np.random.randint(2, size=(size, size))

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[j][i]:
                matrix [i][j] = matrix[j][i]
        matrix[i][i] = 0
    graph = nx.from_numpy_matrix(matrix)

    nx.draw_random(graph)
    plt.show()

grafo()