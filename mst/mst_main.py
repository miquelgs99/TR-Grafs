
# region mst
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

matrix = np.matrix([[0, 3, 0, 0, 5, 0, 4],
                    [3, 0, 1, 0, 0, 0, 0],
                    [0, 1, 0, 5, 0, 8, 0],
                    [0, 0, 5, 0, 0, 0, 0],
                    [5, 0, 0, 0, 0, 4, 0],
                    [0, 0, 8, 0, 4, 0, 5],
                    [4, 0, 0, 0, 0, 5, 0]])

graph = nx.from_numpy_matrix(matrix)

pos = {0: (0, 0),
       1: (2, 0),
       2: (4, 0),
       3: (6, 2),
       4: (0, -4),
       5: (4, -4),
       6: (2, -2)}

nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_labels(graph, pos)
nx.draw_networkx_edges(graph, pos)
edge_labels = nx.get_edge_attributes(graph, "weight")
nx.draw_networkx_edge_labels(graph, pos, edge_labels)
plt.show()

# endregion