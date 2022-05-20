import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def Grafo(*args):

    G = nx.Graph()
    G.clear()

    for i in range(np.random.randint(10, 20)):
        G.add_node(i)
        for j in range(np.random.randint(0, 5)):
            G.add_edge(i, np.random.randint(-20, 20))

    nx.draw_random(G)
    plt.show(block = False)
    plt.savefig(r"C:\Users\garga\Desktop\python\TR-Grafs\Prueba\figure.jpg")
    print("Imagen creada")