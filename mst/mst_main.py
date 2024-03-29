import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

seed = 16

np.random.seed(8)

def create_graph():
    size = 6

    graph = nx.random_tree(size, seed=seed)

    for node in graph.nodes:
        graph.add_edge(node, np.random.randint(size-node-1, size))
        graph.add_edge(node, np.random.randint(size - node - 1, size))

    matrix = nx.to_numpy_array(graph)

    for node in graph.nodes:
        matrix[node][node] = 0

    weight_matrix = np.random.randint(1, 20, size=(size, size))

    matrix = np.multiply(matrix, weight_matrix)

    return nx.from_numpy_matrix(matrix)


graph = create_graph()
for u, v, attr in graph.edges(data=True):
    attr["weight"] = int(round(attr["weight"]))

pos = nx.spring_layout(graph, seed=seed)

nx.draw_networkx_nodes(graph, pos, node_size=1100)
nx.draw_networkx_labels(graph, pos, labels={n: n+1 for n in graph}, font_size=15)
nx.draw_networkx_edges(graph, pos, width=5, alpha=0.8)
edge_labels = nx.get_edge_attributes(graph, "weight")
nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=12)
plt.show()
plt.clf()

sorted_edges = list(graph.edges(data=True))

# Insertion sort
for i in range(1, len(sorted_edges)):

    key = sorted_edges[i]
    j = i - 1
    while j >= 0 and key[2]["weight"] < sorted_edges[j][2]["weight"]:
        sorted_edges[j + 1] = sorted_edges[j]
        j -= 1
    sorted_edges[j + 1] = key

tree_edges = []
connected_components = []

for node in graph.nodes():
    connected_components.append([node])

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

nx.draw_networkx_nodes(graph, pos, node_size=1100)
nx.draw_networkx_labels(graph, pos, labels={n: n+1 for n in graph}, font_size=15)
nx.draw_networkx_edges(graph, pos, edgelist=tree_edges, width=5, alpha=0.8)
tree_edge_labels = {}

for key in edge_labels:
    if key in tree_edges:
        tree_edge_labels[key] = edge_labels[key]

nx.draw_networkx_edge_labels(graph, pos, tree_edge_labels, font_size=12)
plt.show()


