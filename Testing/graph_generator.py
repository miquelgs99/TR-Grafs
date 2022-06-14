import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import *
from tkinter import ttk
PATH_IMAGES = "images"

def grafo(*args):

    size = 10
    matrix = np.random.randint(2, size=(size, size))
    for i in range(len(matrix)):
        matrix[i][i] = 0
    G = nx.from_numpy_matrix(matrix)

    nx.draw_random(G)

    # Creem la direcció de la imatge que guardarem sempre a la carpeta de imatges situada en la carpeta pare de l'actual.
    #my_path = os.path.abspath(os.path.join(os.path.pardir, PATH_IMAGES))  # Figures out the absolute path for you in case your working directory moves around.

    #my_file = "figure.jpg"
    #plt.savefig(os.path.join(my_path, my_file))
    #plt.show(block = False)


