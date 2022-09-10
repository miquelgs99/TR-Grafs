
# region sudoku
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

size = 10

matrix = np.random.randint(-4, 2, size=(size, size))

# We go through the matrix to make it symmetrical and also eliminate the self-connected edges
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] != matrix[j][i]:
            matrix[i][j] = matrix[j][i]

        if matrix[i][j] < 0:
            matrix[i][j] = 0
    matrix[i][i] = 0

isolated_node = 0

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 0:
            isolated_node += 1

    if isolated_node == len(matrix):
        num = (np.random.randint(1, (len(matrix) / 2)))
        for _ in range(num):
            matrix[i][np.random.randint(0, (len(matrix)))] = 1
    isolated_node = 0

node = "".join([str(x) for x in range(size)])
t_ = {}
for i in range(len(matrix)):
    t_[node[i]] = i

# count degree of all node.
degree = []
for i in range(len(matrix)):
    degree.append(sum(matrix[i]))

# initiate the possible color
colorDict = {}
for i in range(len(matrix)):
    colorDict[node[i]] = ["Blue", "Red", "Yellow", "Green"]

# sort the node depends on the degree
sorted_node = []
index = []
# use selection sort
for i in range(len(degree)):
    _max = 0
    j = 0
    for j in range(len(degree)):
        if j not in index:
            if degree[j] > _max:
                _max = degree[j]
                idx = j
    index.append(idx)
    sorted_node.append(node[idx])

# The main process
theSolution = {}
for n in sorted_node:
    setTheColor = colorDict[n]
    theSolution[n] = setTheColor[0]
    adjacentNode = matrix[t_[n]]
    for j in range(len(adjacentNode)):
        if adjacentNode[j] == 1 and (setTheColor[0] in colorDict[node[j]]):
            colorDict[node[j]].remove(setTheColor[0])

G = nx.from_numpy_matrix(matrix)
nx.draw(G, with_labels=True)
plt.show()

# Print the solution
for t, w in sorted(theSolution.items()):
    print("Node", t, " = ", w)

# endregion
