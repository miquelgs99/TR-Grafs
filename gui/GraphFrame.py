from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from grave.style import use_attributes
from grave import plot_network
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import SummaryFrame
import Main
import MenuFrame


class GraphFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        # Declaring variables
        self.node_picker = []
        self.djk_path = []
        self.edges_path = []
        self.solve = 0  # It will be set to 1 if we want to solve the path between nodes
        self.graph = nx.Graph()
        # region GUI

        # region Creating the frames and styling them

        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame', background='green')

        # Create style for the first frame
        s.configure('Frame1.TFrame', background='red')

        # Create separate style for the second frame
        s.configure('Frame2.TFrame', background='blue')

        # Create separate style for the second frame
        s.configure('Frame3.TFrame', background='yellow')

        # We create the frame where the text will be shown
        text_frame = ttk.Frame(self, style='Frame1.TFrame')
        text_frame.grid(column=0, row=0)

        # We create the frame where the graphs will be shown
        graph_frame = ttk.Frame(self, style='Frame2.TFrame')
        graph_frame.grid(column=1, row=0)

        # We create the frame where the nav buttons will be
        nav_frame = ttk.Frame(self, style='Frame3.TFrame')
        nav_frame.grid(column=2, row=1)
        # endregion

        # region Creating the canvas
        self.fig, self.ax = plt.subplots()
        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, padx=20, pady=20)
        # endregion

        # region Creating the labels

        # We put some text explaining what to write in the text box
        vertex_label = ttk.Label(text_frame, text="Introduce the number of vertex that you want: ")
        vertex_label.grid(column=0, row=0, padx=10, pady=10)

        # We create the label where the picked nodes will be
        self.picked_nodes = StringVar()  # The string variable where the label is associated

        picked_nodes_label = ttk.Label(text_frame, textvariable=self.picked_nodes)
        picked_nodes_label.grid(column=2, row=2, padx=10, pady=10)
        # endregion

        # region We create the entry text box

        self.vertex_entry = ttk.Entry(text_frame, width=15)
        self.vertex_entry.grid(column=1, row=0, padx=10, pady=10)
        # endregion

        # region Creating the buttons

        # We create the button that will generate the graph, and we assign the previous function made to it
        generate_button = ttk.Button(text_frame, text="Generate!", command=self.generate_graph)
        generate_button.grid(column=1, row=1, padx=10, pady=10)

        # We create the button that will generate the graph, and we assign the previous function made to it
        dijkstra_button = ttk.Button(text_frame, text="Solve!", command=self.dijkstra)
        dijkstra_button.grid(column=1, row=2, padx=10, pady=10)

        # We create the button that will create the random number, and we assign the previous function made to it
        random_button = ttk.Button(text_frame, text="Random number!",
                                   command=lambda: [self.vertex_entry.delete(0, END),  # Deletes the current value
                                                    self.vertex_entry.insert(
                                                        0, np.random.randint(3, 20)
                                                    )  # Insert new value
                                                    ])
        random_button.grid(column=1, row=3, padx=10, pady=10)

        # We create a button that shut down the program
        quit_button = ttk.Button(text_frame, text="Quit!", command=exit)  # The function exit closes the code directly
        quit_button.grid(column=1, row=4, padx=10, pady=10)
        # endregion

        # region Nav buttons

        nav_button1 = ttk.Button(nav_frame, text="SummaryFrame",
                                 command=lambda: self.new_window(SummaryFrame.SummaryFrame))
        nav_button1.grid(row=0, column=0, padx=10, pady=10)

        nav_button2 = ttk.Button(nav_frame, text="MenuFrame",
                                 command=lambda: self.new_window(MenuFrame.MenuFrame))
        nav_button2.grid(row=0, column=1, padx=10, pady=10)
        # endregion
        # endregion

    # Defining the function that highlights the nodes
    def highlighter(self, event):

        # if we did not hit a node, bail
        if not hasattr(event, 'nodes') or not event.nodes:
            return

        # pull out the graph
        graph = event.artist.graph

        # clear any non-default color on nodes
        for node, attributes in graph.nodes(data=True):
            if len(self.node_picker) == 2:
                if node not in self.djk_path:
                    attributes.pop('color', None)
                else:
                    pass
            else:
                pass

        for u, v, attributes in graph.edges(data=True):
            possible_edges = [(u, v), (v, u)]
            if possible_edges[0] not in self.edges_path and possible_edges[1] not in self.edges_path:
                attributes.pop('width', None)
            else:
                pass

        if len(self.node_picker) == 0:
            self.node_picker.append(event.nodes[0])
        elif len(self.node_picker) == 1:
            if event.nodes[0] == self.node_picker[0]:
                pass
            else:
                self.node_picker.append(event.nodes[0])
        else:
            self.node_picker.clear()
            self.node_picker.append(event.nodes[0])

        for node in event.nodes:
            graph.nodes[node]['color'] = 'red'

        self.picked_nodes.set(str(self.node_picker))

        # update the screen
        event.artist.stale = True
        event.artist.figure.canvas.draw_idle()

    # Defining the function that will generate and show a graph in the GUI
    def generate_graph(self, *args):

        # canvas.get_tk_widget().delete("all")
        if not self.vertex_entry.get().isnumeric() or not int(self.vertex_entry.get()) > 0:
            messagebox.showinfo(title="Error", message="Enter a valid number!")
            return

        self.size = int(self.vertex_entry.get())

        # The matrix of the graph is created with randint from numpy
        matrix = np.random.randint(-100, 20, size=(self.size, self.size))

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
        self.graph = nx.from_numpy_matrix(matrix)

        for node, node_attr in self.graph.nodes(data=True):
            node_attr['size'] = 500

        # ORIGINAL ------------------

        # # We create the figures where the graph will be

        art = plot_network(self.graph, layout="shell", ax=self.ax,
                           node_style=use_attributes(),
                           edge_style=use_attributes(),
                           node_label_style={'font_size': 7,
                                             'font_weight': 'bold',
                                             'font_color': 'k',
                                             'bbox': {'alpha': 0}
                                             })

        # Afegim per sobre el graf etiquetat de forma no interactiva.
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        pos = nx.shell_layout(self.graph)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=8)

        # # I don't know what this does
        art.set_picker(10)
        self.ax.set_title('Click on the nodes!')
        self.fig.canvas.mpl_connect('pick_event', self.highlighter)

        self.canvas.draw()
        # fig.canvas.mpl_connect('pick_event', hlt_refresh)

    def dijkstra(self, *args):

        self.djk_path = nx.dijkstra_path(self.graph, source=self.node_picker[0], target=self.node_picker[1],
                                         weight='weight')

        first = True
        for node in self.djk_path:
            if first:
                first = False
                pass
            else:
                index = self.djk_path.index(node)
                self.edges_path.append((self.djk_path[index - 1], self.djk_path[index]))
            self.graph.nodes[node]['color'] = 'red'
            for edge_attribute in self.graph[node].values():
                edge_attribute['width'] = 3
