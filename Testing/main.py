from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from functools import partial
from grave.style import use_attributes
from grave import plot_network
import numpy as np
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


def random_number(value):
    value.delete(0, END)  # deletes the current value
    value.insert(0, np.random.randint(20))  # inserts new value assigned by 2nd parameter


def show_graph(frame, *args):

    try:
        size = int(vertex_entry.get())
    except ValueError:
        messagebox.showinfo(title="Error", message="Enter a valid number!")

    matrix = np.random.randint(2, size=(size, size))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[j][i]:
                matrix[i][j] = matrix[j][i]
        matrix[i][i] = 0
    graph = nx.from_numpy_matrix(matrix)
    print(graph.number_of_edges())
    nx.draw_random(graph)

    fig, ax = plt.subplots()
    art = plot_network(graph, ax=ax, node_style=use_attributes(),
                       edge_style=use_attributes())

    art.set_picker(10)
    ax.set_title('Click on the nodes!')
    fig.canvas.mpl_connect('pick_event', hilighter)

    canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=1, sticky=(N, W, E, S), padx=20)


root = Tk()
root.title("TR-Grafs")
root.geometry('1280x720')
root.columnconfigure(0, weight=2)
root.rowconfigure(0, weight=2)

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=W)

plot_frame = ttk.Frame(root)
plot_frame.grid(column=0, row=0, sticky=E)

vertex_label = ttk.Label(mainframe, text="Introduce the number of vertex that you want: ")
vertex_label.grid(column=0, row=0, padx=20, pady=20)

vertex_variable = StringVar()

vertex_entry = ttk.Entry(mainframe, width=15, textvariable=vertex_variable)
vertex_entry.grid(column=1, row=0, padx=0, pady=20)

show_graph_with_arg = partial(show_graph, plot_frame)

generate_button = ttk.Button(mainframe, text="Generate!", command=show_graph_with_arg)
generate_button.grid(column=1, row=1)

random_number_with_arg = partial(random_number, vertex_entry)

random_button = ttk.Button(mainframe, text="Random number!", command=random_number_with_arg)
random_button.grid(column=1, row=2)

quit_button = ttk.Button(mainframe, text="Quit!", command=exit)
quit_button.grid(column=1, row=3, pady=10)

root.bind("<Return>", show_graph_with_arg)
vertex_entry.focus()
root.mainloop()


