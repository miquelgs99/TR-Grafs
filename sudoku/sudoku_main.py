import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

size = 10

matrix = np.random.randint(1, 2, size=(size, size))

isolated_node = 0

for i in range(len(matrix)):
    for j in range(len(matrix[i])):

        if matrix[i][j] != matrix[j][i]:
            matrix[i][j] = matrix[j][i]

        if matrix[i][j] < 0:
            matrix[i][j] = 0

        if matrix[i][j] == 0:
            isolated_node += 1

    if isolated_node == len(matrix):
        rep = (np.random.randint(1, len(matrix)))
        for _ in range(rep):
            # try:
            #     matrix[i][i+1] = 1
            # except IndexError:
            #     matrix[i][i-1] = 1
            matrix[i][np.random.randint(0, (len(matrix)))] = 1
    isolated_node = 0
    matrix[i][i] = 0

pprint(matrix)

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
    colorDict[node[i]] = ["#eb34eb", "#ADD8E6", "Red", "Yellow",
                          "Green", "#eba234", "#5e0000", "#0008ff",
                          "#0088ff", "#ff82ac"]

# sort the node depends on the degree
sorted_node = []
index = []
# use selection sort
for i in range(len(degree)):
    _max = 0
    j = 0
    for j in range(len(degree)):
        if j not in index:
            if degree[j] >= _max:
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

# for t, w in sorted(theSolution.items()):
#     print("Node", t, " = ", w)

sorted_solution = dict(sorted(theSolution.items()))
colors = []
for node, color in sorted_solution.items():
    colors.append(color)

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=250, node_color=colors)
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos, labels={n: n + 1 for n in G})
plt.show()