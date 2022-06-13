import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

G = nx.Graph()

for i in range(np.random.randint(10, 20)):
    G.add_node(i)
    for j in range(np.random.randint(0, 5)):
        G.add_edge(i, np.random.randint(-20, 20))

nx.draw_random(G)
plt.savefig(r"C:\Users\garga\Desktop\python\TR-Grafs\Prueba\figure.jpg")