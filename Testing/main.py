from tkinter import *
from tkinter import ttk
import time
import os.path
import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import graph_generator
from functools import partial

from grave.style import use_attributes

from grave import plot_network
import numpy as np

import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


def hilighter(event):
    # if we did not hit a node, bail
    if not hasattr(event, 'nodes') or not event.nodes:
        return

    # pull out the graph,
    graph = event.artist.graph

    # clear any non-default color on nodes
    for node, attributes in graph.nodes.data():
        attributes.pop('color', None)

    for u, v, attributes in graph.edges.data():
        attributes.pop('width', None)

    for node in event.nodes:
        graph.nodes[node]['color'] = 'C1'

        for edge_attribute in graph[node].values():
            edge_attribute['width'] = 3

    # update the screen
    event.artist.stale = True
    event.artist.figure.canvas.draw_idle()


def GenerarGrafo(mainframe, *args):
    size = 10
    matrix = np.random.randint(2, size=(size, size))
    for i in range(len(matrix)):
        matrix[i][i] = 0
    graph = nx.from_numpy_matrix(matrix)

    nx.draw_random(graph)

    fig, ax = plt.subplots()
    art = plot_network(graph, ax=ax, node_style=use_attributes(),
                       edge_style=use_attributes())

    art.set_picker(10)
    ax.set_title('Click on the nodes!')
    fig.canvas.mpl_connect('pick_event', hilighter)

    canvas = FigureCanvasTkAgg(fig, master=mainframe)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=1)

    # plt.cla()
    # graph_generator.grafo()


root = Tk()
root.title("TR-Grafs")
root.geometry('660x750')
# root.resizable(0, 0)

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=2)
mainframe.rowconfigure(0, weight=2)

num_vertex = StringVar()

MainEntry = ttk.Entry(mainframe, textvariable=num_vertex, width=15)
MainEntry.grid(column=1, row=0, padx=20, pady=20)

action_with_arg = partial(GenerarGrafo, root)

GenerateButton = ttk.Button(mainframe, text="Generate!", command=action_with_arg)
GenerateButton.grid(column=1, row=1)

# Creem la direcció de la imatge que guardarem sempre a la carpeta de imatges situada en la carpeta pare de l'actual.

# my_file = "figure.jpg"
# image_path = os.path.join(os.path.join(os.path.pardir,graph_generator.PATH_IMAGES), my_file)
# Img = ImageTk.PhotoImage(Image.open(image_path))
# ImgLabel = ttk.Label(mainframe, image=Img)
# ImgLabel.grid(column=1, row=3, padx=10)


# for child in mainframe.winfo_children():
#   child.grid_configure(padx=5, pady=5)

root.bind("<Return>", action_with_arg)
MainEntry.focus()
root.mainloop()
