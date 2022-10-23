import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

size = 20


def create_graph():
    graph = nx.random_tree(size)

    for vertex in graph.nodes:
        n = np.random.randint(5)
        for _ in range(n):
            graph.add_edge(vertex, np.random.randint(size - vertex - 1, size))
            # graph.add_edge(vertex, np.random.randint(0, size))

    return nx.to_numpy_array(graph)


matrix = create_graph()
for i in range(len(matrix)):
    matrix[i][i] = 0

node = [str(x) for x in range(size)]
t_ = {}
for i in range(len(matrix)):
    t_[node[i]] = i

# count degree of all node.
degree = [sum(matrix[i]) for i in range(len(matrix))]

# initiate the possible color

color_dict = {}

for i in range(len(matrix)):
    color_dict[node[i]] = ['#e6194b',
                           '#3cb44b',
                           '#ffe119',
                           '#4363d8',
                           '#f58231',
                           '#911eb4',
                           '#46f0f0',
                           '#f032e6',
                           '#bcf60c',
                           '#fabebe',
                           '#008080',
                           '#e6beff',
                           '#9a6324',
                           '#fffac8',
                           '#800000',
                           '#aaffc3',
                           '#808000',
                           '#ffd8b1',
                           '#000075',
                           '#808080']

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

# The main process
solution = {}

for u in sorted_node:
    p = color_dict[u]
    for v in sorted_node:
        if matrix[int(u)][int(v)] == 1 and v in solution:
            if solution[v] in p:
                p.remove(solution[v])
    solution[u] = p[0]

print(solution)
G = nx.from_numpy_matrix(matrix)

for key in solution.copy().keys():
    solution[int(key)] = solution.pop(key)

sorted_solution = dict(sorted(solution.items()))
colors = []

for nodes, color in sorted_solution.items():
    colors.append(color)

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=250, node_color=colors)
nx.draw_networkx_edges(G, pos, width=2)
# nx.draw_networkx_labels(G, pos, labels={n: n + 1 for n in G})
nx.draw_networkx_labels(G, pos, labels={n: n for n in G})

# for t, w in sorted_solution.items():
#     print("Node",t," = ",w)
plt.show()










