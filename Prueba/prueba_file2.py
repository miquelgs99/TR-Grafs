import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
PATH_IMAGES= "images"

def Grafo(*args):

    G = nx.Graph()
    G.clear()

    for i in range(np.random.randint(10, 20)):
        G.add_node(i)
        for j in range(np.random.randint(0, 5)):
            G.add_edge(i, np.random.randint(-20, 20))

    nx.draw_random(G)

    # Creem la direcció de la imatge que guardarem sempre a la carpeta de imatges situada en la carpeta pare de l'actual.
    my_path = os.path.abspath(os.path.join(os.path.pardir,PATH_IMAGES))  # Figures out the absolute path for you in case your working directory moves around.

    my_file = "figure.jpg"

    plt.savefig(os.path.join(my_path, my_file))
    print("Imagen creada")
    plt.show(block = False)


