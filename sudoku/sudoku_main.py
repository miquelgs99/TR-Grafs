import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

size = 500


def create_graph():
    graph = nx.random_tree(size)

    for v in graph.nodes:
        graph.add_edge(v, np.random.randint(size - v - 1, size))

    return nx.to_numpy_array(graph)


matrix = create_graph()

for i in range(len(matrix)):
    matrix[i][i] = 0

print([str(x) for x in range(size)])

node = [str(x) for x in range(size)]
t_ = {}
for i in range(len(matrix)):
    t_[node[i]] = i

# count degree of all node.
degree = [sum(matrix[i]) for i in range(len(matrix))]

# initiate the possible color
colorDict = {}
for i in range(len(matrix)):
    colorDict[node[i]] = ["#eb34eb",
                          "#ADD8E6",
                          "Red",
                          "Yellow",
                          "Green",
                          "#eba234",
                          "#5e0000",
                          "#0008ff",
                          "#0888ff",
                          "#ff82ac",
                          "#0303ff",
                          "#0303fc"]


# sort the node depends on the degree

sorted_node = []
index = []

# use selection sort
for i in range(len(degree)):
    _max = 0
    idx = 0
    for j in range(len(degree)):
        if j not in index:
            if degree[j] >= _max:
                _max = degree[j]
                idx = j
    index.append(idx)
    sorted_node.append(node[idx])

print(degree)


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

sorted_solution = dict(sorted(theSolution.items()))
colors = []
for node, color in sorted_solution.items():
    colors.append(color)

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=250, node_color=colors)
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos, labels={n: n + 1 for n in G})
plt.show()
