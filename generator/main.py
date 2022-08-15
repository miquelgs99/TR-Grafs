from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from functools import partial                                 # Import libraries
from grave.style import use_attributes
from grave import plot_network
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import pprint

solve = 0           # It will be set to 1 if we want to solve the path between nodes
edges_path = []


# Per solucionar errors ens aniria molt bé poder fer que les actualitzacions de color i gruix dels nodes i arestes
# estiguessin fora de la funció highlighter, perquè el que passa es que només es pinta el camí quan cliques a un node.
# Hauria d'intentar que tot el que tinc ara a highlighter estigués a una funció dijkstra que s'estigués executant tota
# l'estona o algo així, o que el jeroni si sap faci alguna forma per actualitzar el widget tota l'estona (sense funció)

# Defining the function that highlights the nodes
def highlighter(event):

    global edges_path
    global solve
    global djk_path
    global graph
    if solve == 1:      # Check if we want to solve the path
        solve = 0
        djk_path = nx.dijkstra_path(graph, source=node_picker[0], target=node_picker[1], weight='weight')

        first = True
        for node in djk_path:
            if first:
                first = False
                pass
            else:
                index = djk_path.index(node)
                edges_path.append((djk_path[index - 1], djk_path[index]))
            graph.nodes[node]['color'] = 'red'
            for edge_attribute in graph[node].values():
                edge_attribute['width'] = 3

        event.artist.stale = True
        event.artist.figure.canvas.draw_idle()


    # if we did not hit a node, bail
    if not hasattr(event, 'nodes') or not event.nodes:
        return

    # pull out the graph,
    graph = event.artist.graph

    # clear any non-default color on nodes
    for node, attributes in graph.nodes(data=True):
        if len(node_picker) == 2:
            if node not in djk_path:
                attributes.pop('color', None)
            else:
                pass
        else:
            pass

    for u, v, attributes in graph.edges(data=True):
        possible_edges = [(u, v), (v, u)]
        if possible_edges[0] not in edges_path and possible_edges[1] not in edges_path:
            attributes.pop('width', None)
        else:
            pass

    if len(node_picker) == 0:
        node_picker.append(event.nodes[0])
    elif len(node_picker) == 1:
        if event.nodes[0] == node_picker[0]:
            pass
        else:
            node_picker.append(event.nodes[0])
    else:
        node_picker.clear()
        node_picker.append(event.nodes[0])

    for node in event.nodes:
        graph.nodes[node]['color'] = 'red'

    picked_nodes.set(str(node_picker))

    # update the screen
    event.artist.stale = True
    event.artist.figure.canvas.draw_idle()


# Defining the function that will generate and show a graph in the GUI
def show_graph(frame, *args):

    # canvas.get_tk_widget().delete("all")
    try:
        if int(vertex_entry.get()) > 0:
            size = int(vertex_entry.get())
        else:
            messagebox.showinfo(title="Error", message="Enter a valid number!")
    except ValueError:
        messagebox.showinfo(title="Error", message="Enter a valid number!")

    # The matrix of the graph is created with randint from numpy
    matrix = np.random.randint(-100, 20, size=(size, size))

    # We go through the matrix to make it symmetrical and also eliminate the self-connected edges
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[j][i]:
                matrix[i][j] = matrix[j][i]

            if matrix[i][j] < 0:
                matrix[i][j] = 0
        matrix[i][i] = 0
    matrix[0][2] = 0

    # We create the graph from the matrix
    global graph
    graph = nx.from_numpy_matrix(matrix)

    for node, node_attr in graph.nodes(data=True):
        node_attr['size'] = 500

    # ORIGINAL ------------------

    # # We create the figures where the graph will be

    art = plot_network(graph, layout="shell", ax=ax,
                       node_style=use_attributes(),
                       edge_style=use_attributes(),
                       node_label_style={'font_size': 7,
                                         'font_weight': 'bold',
                                         'font_color': 'k',
                                         'bbox': {'alpha': 0}
                                         })

    # Afegim per sobre el graf etiquetat de forma no interactiva.
    edge_labels = nx.get_edge_attributes(graph, "weight")
    pos = nx.shell_layout(graph)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=8)

    # # I don't know what this does
    art.set_picker(10)
    ax.set_title('Click on the nodes!')
    fig.canvas.mpl_connect('pick_event', highlighter)

    canvas.draw()
    # We create a canvas with the figure, and we put it in the GUI


def dijkstra(*args):

    global solve
    solve = True
    # node_picker = []
    # djk_path = nx.dijkstra_path(graph, source=node_picker[0], target=node_picker[1], weight='weight')
    #
    # for node in djk_path:
    #     graph.nodes[node]['color'] = 'red'
    #     for edge_attribute in graph[node].values():
    #         edge_attribute['width'] = 3
    #
    # canvas.draw()


# Declaring variables
node_picker = []
djk_path = []


# region We create the main window, and we define some characteristics
root = Tk()
root.title("TR-Grafs")
root.geometry('1280x720')
root.columnconfigure(0, weight=2)   # We define the grid that the window will have
root.rowconfigure(0, weight=2)      # We define the grid that the window will have
# endregion

# region Creating the frames
# We create the frame where the text will be shown
text_frame = ttk.Frame(root)
text_frame.grid(column=0, row=0, sticky=W)

# We create the frame where the graphs will be shown
graph_frame = ttk.Frame(root)
graph_frame.grid(column=0, row=0, sticky=E)
# endregion

fig, ax = plt.subplots()
plt.axis('off')
canvas = FigureCanvasTkAgg(fig, master=graph_frame)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=1, sticky=(N, W, E, S), padx=20)

# region Creating the labels

# We put some text explaining what to write in the text box
vertex_label = ttk.Label(text_frame, text="Introduce the number of vertex that you want: ")
vertex_label.grid(column=0, row=0, padx=20, pady=20)

# We create the label where the picked nodes will be
picked_nodes = StringVar()    # The string variable where the label is associated

picked_nodes_label = ttk.Label(text_frame, textvariable=picked_nodes)
picked_nodes_label.grid(column=2, row=2, padx=20, pady=20)

# endregion

# region We create the entry text box

vertex_entry = ttk.Entry(text_frame, width=15)
vertex_entry.grid(column=1, row=0, padx=0, pady=20)

# endregion

# region Creating the buttons

# We create the button that will generate the graph, and we assign the previous function made to it
generate_button = ttk.Button(text_frame, text="Generate!", command=lambda: show_graph(graph_frame))
generate_button.grid(column=1, row=1)

# We create the button that will generate the graph, and we assign the previous function made to it
dijkstra_button = ttk.Button(text_frame, text="Solve!", command=dijkstra)
dijkstra_button.grid(column=1, row=2)

# We create the button that will create the random number, and we assign the previous function made to it
random_button = ttk.Button(text_frame, text="Random number!",
                           command=lambda: [vertex_entry.delete(0, END),  # Deletes the current value
                                            vertex_entry.insert(0, np.random.randint(3, 20))  # Inserts new value
                                            ])
random_button.grid(column=1, row=3)

# We create a button that shut down the program
quit_button = ttk.Button(text_frame, text="Quit!", command=exit)  # The function exit closes the code directly
quit_button.grid(column=1, row=4)

# endregion


vertex_entry.focus()       # We focus the text writing in the text box when initializing the code
root.mainloop()


