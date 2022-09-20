import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# matrix = np.matrix([[0, 3, 0, 0, 5, 0, 4],
#                     [3, 0, 1, 0, 0, 0, 0],
#                     [0, 1, 0, 5, 0, 8, 0],
#                     [0, 0, 5, 0, 0, 0, 0],
#                     [5, 0, 0, 0, 0, 4, 0],
#                     [0, 0, 8, 0, 4, 0, 5],
#                     [4, 0, 0, 0, 0, 5, 0]])

matrix = np.random.randint(-10, 20, size=(15, 15))

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] != matrix[j][i]:
            matrix[i][j] = matrix[j][i]

        if matrix[i][j] < 0:
            matrix[i][j] = 0
    matrix[i][i] = 0

graph = nx.from_numpy_matrix(matrix)

# pos = {0: (0, 0),
#        1: (2, 0),
#        2: (4, 0),
#        3: (6, 2),
#        4: (0, -4),
#        5: (4, -4),
#        6: (2, -2)}

pos = nx.spring_layout(graph)

nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_labels(graph, pos)
nx.draw_networkx_edges(graph, pos)
edge_labels = nx.get_edge_attributes(graph, "weight")
nx.draw_networkx_edge_labels(graph, pos, edge_labels)
plt.show()
plt.clf()


sorted_edges = list(graph.edges(data=True))

# Insertion sort
for i in range(1, len(sorted_edges)):

    key = sorted_edges[i][2]["weight"]
    j = i - 1
    while j >= 0 and key < sorted_edges[j][2]["weight"]:
        sorted_edges[j + 1][2]["weight"] = sorted_edges[j][2]["weight"]
        j -= 1
    sorted_edges[j + 1][2]["weight"] = key

tree_edges = []
connected_components = []

for node in graph.nodes():
    connected_components.append([node])
print(connected_components)

for u, v, attr in sorted_edges:
    u_list = 0
    v_list = 0
    for idx, comp in enumerate(connected_components):
        if u in comp:
            u_list = idx
        if v in comp:
            v_list = idx
    if u_list != v_list:
        tree_edges.append((u, v))
        connected_components[u_list] = connected_components[u_list] + connected_components[v_list]
        connected_components.pop(v_list)

nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_labels(graph, pos)
nx.draw_networkx_edges(graph, pos, edgelist=tree_edges)
tree_edge_labels = {}

for key in edge_labels:
    if key in tree_edges:
        tree_edge_labels[key] = edge_labels[key]
nx.draw_networkx_edge_labels(graph, pos, tree_edge_labels)
plt.show()
