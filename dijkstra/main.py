import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

matrix = np.random.randint(-100, 20, size=(3, 3))

G = nx.Graph()

G = nx.from_numpy_matrix(matrix)

nx.draw(G)
plt.show()


