from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from grave.style import use_attributes
from grave import plot_network
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import SudokuColoringFrame
import Main
import MenuFrame
import time


class GraphFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        # self.configure(width=1180, height=710)
        self.grid(sticky="nswe")

        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        # Declaring variables
        self.node_picker = []
        self.djk_path = []
        self.edges_path = []
        self.path_exists = False  # It will be set to 1 if there's a path drawn
        self.graph = nx.Graph()

        # region GUI

        # We create the frame where the text will be shown
        text_frame = ctk.CTkFrame(self, corner_radius=0)
        text_frame.grid(column=0, row=0, sticky="nswe", rowspan=2)

        # We create the frame where the graphs will be shown
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(column=1, row=0, padx=10)

        # We create the frame where the nav buttons will be
        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(column=1, row=1, padx=20, sticky="E")
        # endregion

        self.cid=0
        self.create_canvas()

        # region Creating the labels

        # We put some text explaining what to write in the text box
        vertex_label = ctk.CTkLabel(text_frame, text="Quants vèrtexs tindrà el graf?", text_font=("helvetica", 12))
        vertex_label.grid(column=0, row=0, padx=10, pady=10)

        self.picked_nodes = StringVar()  # The string variable where the label is associated
        # picked_nodes_label = ctk.CTkLabel(text_frame, textvariable=self.picked_nodes)
        # picked_nodes_label.grid(column=2, row=2, padx=10, pady=10)

        # endregion

        # region We create the entry text box

        self.vertex_entry = ctk.CTkEntry(text_frame, width=50)
        self.vertex_entry.grid(column=0, row=1, padx=10, pady=10)
        # endregion

        # region Creating the buttons

        # We create the button that will generate the graph, and we assign the previous function made to it
        self.generate_button = ctk.CTkButton(text_frame,
                                        text="Generar graf!",
                                        text_font=("helvetica", 12),
                                        width=120,
                                        height=32,
                                        corner_radius=8,
                                        text_color="black",
                                        command=self.show_graph)
        self.generate_button.grid(column=0, row=2, padx=10, pady=10)

        # We create the button that will generate the graph, and we assign the previous function made to it
        self.dijkstra_button = ctk.CTkButton(text_frame,
                                        text="Trobar camí!",
                                        text_font=("helvetica", 12),
                                        width=120,
                                        height=32,
                                        corner_radius=8,
                                        text_color="black",
                                        command=self.dijkstra)
        self.dijkstra_button.grid(column=0, row=3, padx=10, pady=10)

        # We create the button that will create the random number, and we assign the previous function made to it
        self.random_button = ctk.CTkButton(text_frame,
                                      text="Nombre aleatori!",
                                      text_font=("helvetica", 12),
                                      width=120,
                                      height=32,
                                      corner_radius=8,
                                      text_color="black",
                                      command=lambda: [self.vertex_entry.delete(0, END),  # Deletes the current value
                                                    self.vertex_entry.insert(
                                                        0, np.random.randint(3, 20)
                                                    )  # Insert new value
                                                    ])
        self.random_button.grid(column=0, row=4, padx=10, pady=10)

        # endregion

        # region Nav buttons

        nav_button2 = ctk.CTkButton(nav_frame,
                                    text="Menú principal",
                                    width=120,
                                    height=32,
                                    corner_radius=8,
                                    text_color="black",
                                    command=lambda: self.new_window(MenuFrame.MenuFrame))
        nav_button2.grid(row=0, column=1, padx=10, pady=10, sticky="E")
        # endregion
        # endregion

    def create_canvas(self):
        """
        Draws/redraws a canvas on which to draw graphs on.
        :return:
        """
        # try:
        #     self.canvas.get_tk_widget().destroy()
        # except AttributeError:
        #     pass

        self.fig, self.ax = plt.subplots()
        self.fig.set_figheight(5.5)
        self.fig.set_figwidth(9.75)

        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(column=0, row=0, padx=20, pady=20, sticky="E")
        self.canvas.draw()

    # Defining the function that highlights the nodes
    def highlighter(self, event):

        # if we did not hit a node, bail
        if not hasattr(event, 'nodes') or not event.nodes:
            return

        # pull out the graph
        self.graph = event.artist.graph

        # clear any non-default color on nodes
        for node, attributes in self.graph.nodes(data=True):
            if len(self.node_picker) == 2:
                attributes.pop('color', None)
            if node in self.djk_path:
                attributes.pop('color', None)

        for u, v, attributes in self.graph.edges(data=True):
            attributes.pop('width', None)

            # possible_edges = [(u, v), (v, u)]
            # if possible_edges[0] not in self.edges_path and possible_edges[1] not in self.edges_path:
            #     attributes.pop('width', None)
            # else:
            #     pass

        if self.path_exists:
            self.djk_path = []
            self.path_exists = False

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
            self.graph.nodes[node]['color'] = 'red'

        self.picked_nodes.set(str(self.node_picker))

        # update the screen
        event.artist.stale = True
        event.artist.figure.canvas.draw_idle()

    # Defining the function that will create a graph from the entry
    def create_graph(self):
        graph = nx.random_tree(self.size)

        for node in graph.nodes:

            if 1 < node < (len(graph.nodes)-1):
                graph.add_edge(node, np.random.randint(node-2, node+2))
            else:
                if node < (len(graph.nodes)-1):
                    graph.add_edge(node, np.random.randint(node, node+2))
                else:
                    graph.add_edge(node, np.random.randint(node-2, node))

        matrix = nx.to_numpy_array(graph)

        for node in graph.nodes:
            matrix[node][node] = 0

        weight_matrix = np.random.randint(1, 20, size=(self.size, self.size))
        matrix = np.multiply(matrix, weight_matrix)

        return nx.from_numpy_matrix(matrix)

    # Defining the function that will plot the graph in matplotlib
    def plot_graph(self):
        for node, node_attr in self.graph.nodes(data=True):
            node_attr['size'] = 500

        for u, v, attr in self.graph.edges(data=True):
            attr["weight"] = int(round(attr["weight"]))

        if self.cid:
            self.canvas.mpl_disconnect(self.cid)
            self.art.set_picker(None)
        self.art = plot_network(self.graph, layout="shell", ax=self.ax,
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

        self.art.set_picker(10)
        self.cid = self.canvas.mpl_connect('pick_event', self.highlighter)

        self.canvas.draw()

    # Defining the function that will show the graph in the GUI
    def show_graph(self):

        if not self.vertex_entry.get().isnumeric() or not int(self.vertex_entry.get()) > 0:
            # messagebox.showinfo(title="Error", message="Enter a valid number!")
            self.pop_error("Error", "Introdueix un nombre vàlid!")
            return

        self.create_canvas()
        self.node_picker = []
        self.picked_nodes.set(str(self.node_picker))

        self.size = int(self.vertex_entry.get())

        self.graph = self.create_graph()

        # We create the figures where the graph will be
        self.plot_graph()


    def dijkstra(self, *args):
        try:
            try:
                st = time.time()
                self.djk_path = nx.dijkstra_path(self.graph, source=self.node_picker[0], target=self.node_picker[1],
                                                 weight='weight')
                et = time.time()
                elapsed_time = et - st
                print('Execution time:', elapsed_time, 'seconds')
            except IndexError:
                # messagebox.showinfo(title="Error", message="Select two nodes.", sex="jdkfj")
                self.pop_error("Error", "Selecciona dos nodes.")
                return
        except nx.exception.NetworkXNoPath:
            # messagebox.showinfo(title="Oh!", message="There's no path between these nodes. Select another ones.")
            self.pop_error("Oh!", "No hi ha cap camí entre aquests dos nodes. Selecciona uns altres")
            return

        self.node_picker = []
        self.picked_nodes.set(str(self.node_picker))

        first = True

        # TODO: Reduce this to simply highlighting the nodes and edges in the graph
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

        # Remove edges that are not in the path
        for u, v, attributes in self.graph.edges(data=True):
            possible_edges = [(u, v), (v, u)]
            if possible_edges[0] not in self.edges_path and possible_edges[1] not in self.edges_path:
                attributes.pop('width', None)
            else:
                pass

        self.path_exists = True
        self.plot_graph()
