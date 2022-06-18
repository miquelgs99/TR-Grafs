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


# Defining the function that highlights the nodes
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


# Defining the function that generates a random number in the text entry
def random_number(value):
    value.delete(0, END)  # deletes the current value
    value.insert(0, np.random.randint(20))  # inserts new value assigned by 2nd parameter


# Defining the function that will generate and show a graph in the GUI
def show_graph(frame, *args):
    try:
        # If the text in the entry is an integer, we set the size of the graph to the number entered
        size = int(vertex_entry.get())
    except ValueError:
        # If not, the code detects the error and shows an error messagebox
        messagebox.showinfo(title="Error", message="Enter a valid number!")

    # The matrix of the graph is created with randint from numpy
    matrix = np.random.randint(2, size=(size, size))

    # We go through the matrix to make it symmetrical and also eliminate the self-connected edges
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[j][i]:
                matrix[i][j] = matrix[j][i]
        matrix[i][i] = 0

    # We create the graph and we draw it randomly
    graph = nx.from_numpy_matrix(matrix)
    nx.draw_random(graph)

    # We create the figures where the graph will be
    fig, ax = plt.subplots()
    art = plot_network(graph, ax=ax, node_style=use_attributes(),
                       edge_style=use_attributes())

    # I don't know what this does
    art.set_picker(10)
    ax.set_title('Click on the nodes!')
    fig.canvas.mpl_connect('pick_event', hilighter)

    # We create a canvas with the figure and we put it in the GUI
    canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=1, sticky=(N, W, E, S), padx=20)


# We create the main window and we define some characteristics
root = Tk()
root.title("TR-Grafs")
root.geometry('1280x720')
root.columnconfigure(0, weight=2)   # We define the grid that the window will have
root.rowconfigure(0, weight=2)      # We define the grid that the window will have

# We create the frame where the text will be shown
text_frame = ttk.Frame(root)
text_frame.grid(column=0, row=0, sticky=W)

# We create the frame where the graphs will be shown
graph_frame = ttk.Frame(root)
graph_frame.grid(column=0, row=0, sticky=E)

# We put some text explaining what to write in the text box
vertex_label = ttk.Label(text_frame, text="Introduce the number of vertex that you want: ")
vertex_label.grid(column=0, row=0, padx=20, pady=20)

# We create the entry text box
vertex_entry = ttk.Entry(text_frame, width=15)
vertex_entry.grid(column=1, row=0, padx=0, pady=20)

# We use the partial function to create another function from show_graph that already has the args in
# We need this because tkinter buttons cannot take args when a standard function to them is assigned
show_graph_with_arg = partial(show_graph, graph_frame)

# We create the button that will generate the graph, and we assign the previous function made to it
generate_button = ttk.Button(text_frame, text="Generate!", command=show_graph_with_arg)
generate_button.grid(column=1, row=1)

# We do the same with the random_number function that we did before
random_number_with_arg = partial(random_number, vertex_entry)

# We create the button that will create the random number, and we assign the previous function made to it
random_button = ttk.Button(text_frame, text="Random number!", command=random_number_with_arg)
random_button.grid(column=1, row=2)

# We create a button that shut down the program
quit_button = ttk.Button(text_frame, text="Quit!", command=exit) # The function exit closes the code directly
quit_button.grid(column=1, row=3, pady=10)

root.bind("<Return>", show_graph_with_arg)  # We assign the function that generates the graph to the return key
vertex_entry.focus()                        # We focus the text writing in the text box when initializing the code
root.mainloop()


