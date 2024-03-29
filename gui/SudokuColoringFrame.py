from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from grave.style import use_attributes
from grave import plot_network
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Main
import GraphFrame
import MenuFrame
import SudokuFrame
from pprint import pprint


class SudokuColoringFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        self.grid(sticky="nswe")

        self.size = 0
        self.colors = []
        self.graph = nx.Graph()
        self.pos = None

        self.text_frame = ctk.CTkFrame(self, corner_radius=0)
        self.text_frame.grid(column=0, row=0, sticky="nsw", rowspan=3)

        top_text_frame = ctk.CTkFrame(self)
        top_text_frame.grid(column=1, row=0, padx=10, pady=10)

        self.coloring_frame = ctk.CTkFrame(self)
        self.coloring_frame.grid(column=1, row=1, padx=20, sticky="nswe")

        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(column=1, row=2, padx=20, pady=10, sticky="we")
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)

        self.create_canvas()

        self.create_buttons()

        self.which_frame = "Coloring"

        self.left_label = ctk.CTkButton(top_text_frame,
                                        text='Coloració',
                                        text_font=('Segoe UI', 15),
                                        text_color="#383838",
                                        bg_color="#383838",
                                        fg_color="#383838",
                                        hover=False,
                                        command=(lambda: self.change_to("left")))
        self.left_label.grid(column=0, row=0, padx=20)

        self.mid_label = ctk.CTkLabel(top_text_frame,
                                      text='Coloració',
                                      text_font=('Segoe UI', 20))
        self.mid_label.grid(column=1, row=0, padx=20, pady=10)

        self.right_label = ctk.CTkButton(top_text_frame,
                                         text='Sudoku',
                                         text_font=('Segoe UI', 15),
                                         bg_color="#383838",
                                         fg_color="#383838",
                                         hover=False,
                                         command=(lambda: self.change_to("right")))
        self.right_label.grid(column=2, row=0, padx=20)

        nav_button1 = ctk.CTkButton(nav_frame,
                                    text="Menú principal",
                                    width=120,
                                    height=32,
                                    corner_radius=8,
                                    text_color="black",
                                    command=lambda: self.new_window(MenuFrame.MenuFrame))
        nav_button1.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # endregion

    def change_to(self, btn, event=None):

        if self.which_frame == "Coloring" and btn == "right":
            self.left_label.configure(text_color="white")
            self.mid_label.configure(text='Sudoku')
            self.right_label.configure(text_color="#383838")
            self.which_frame = "Sudoku"

            self.erase_buttons()
            self.create_canvas()
            self.sudoku_frame = SudokuFrame.SudokuFrame(self, 9, self.text_frame)
            self.sudoku_frame.grid(column=1, row=1)
            self.sudoku_frame.tkraise()

        elif self.which_frame == "Sudoku" and btn == "left":
            self.left_label.configure(text_color="#383838")
            self.mid_label.configure(text='Coloració')
            self.right_label.configure(text_color="white")
            self.which_frame = "Coloring"

            self.sudoku_frame.erase_buttons()
            self.create_buttons()
            self.coloring_frame.tkraise()

    def erase_buttons(self):
        self.generate_button.destroy()
        self.color_button.destroy()
        self.random_button.destroy()
        self.vertex_label.destroy()
        self.vertex_entry.destroy()

    def create_buttons(self):

        self.vertex_label = ctk.CTkLabel(self.text_frame, text="Quants vèrtexs tindrà el graf?",
                                         text_font=("helvetica", 12))
        self.vertex_label.grid(column=0, row=0, padx=10, pady=10)

        self.vertex_entry = ctk.CTkEntry(self.text_frame, width=50)
        self.vertex_entry.grid(column=0, row=1, padx=10, pady=10)

        self.generate_button = ctk.CTkButton(self.text_frame,
                                             text="Generar graf!",
                                             text_font=("helvetica", 12),
                                             width=120,
                                             height=32,
                                             corner_radius=8,
                                             text_color="black",
                                             command=self.show_graph)
        self.generate_button.grid(column=0, row=2, padx=10, pady=10)

        self.color_button = ctk.CTkButton(self.text_frame,
                                          text="Pintar graf!",
                                          text_font=("helvetica", 12),
                                          width=120,
                                          height=32,
                                          corner_radius=8,
                                          text_color="black",
                                          command=self.color_graph)
        self.color_button.grid(column=0, row=3, padx=10, pady=10)

        self.random_button = ctk.CTkButton(self.text_frame,
                                           text="Nombre aleatori!",
                                           text_font=("helvetica", 12),
                                           width=120,
                                           height=32,
                                           corner_radius=8,
                                           text_color="black",
                                           command=lambda: [self.vertex_entry.delete(0, END),
                                                            # Deletes the current value
                                                            self.vertex_entry.insert(
                                                                0, np.random.randint(3, 20)
                                                            )  # Insert new value
                                                            ])
        self.random_button.grid(column=0, row=4, padx=10, pady=10)

    def create_canvas(self):
        """
        Draws/redraws a canvas on which to draw graphs on.
        :return:
        """
        try:
            self.canvas.get_tk_widget().destroy()
        except AttributeError:
            pass

        self.fig, self.ax = plt.subplots()
        self.fig.set_figheight(5)
        self.fig.set_figwidth(9)
        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.coloring_frame)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(column=0, row=0, padx=20, pady=20)
        self.canvas.draw()

    def create_graph(self):
        # The matrix of the graph is created with randint from numpy
        graph = nx.random_tree(self.size)

        for v in graph.nodes:
            graph.add_edge(v, np.random.randint(self.size - v - 1, self.size))

        matrix = nx.to_numpy_array(graph)

        for node in graph.nodes:
            matrix[node][node] = 0

        return nx.from_numpy_matrix(matrix)

    # Defining the function that will plot the graph in matplotlib
    def plot_graph(self):

        for node, node_attr in self.graph.nodes(data=True):
            node_attr['size'] = 500

        # art = plot_network(self.graph, layout="spring", ax=self.ax,
        #                    node_style=use_attributes(),
        #                    edge_style=use_attributes(),
        #                    node_label_style={'font_size': 7,
        #                                      'font_weight': 'bold',
        #                                      'font_color': 'k',
        #                                      'bbox': {'alpha': 0}
        #                                      })

        pos = nx.spring_layout(self.graph)
        self.pos = pos

        nx.draw_networkx_nodes(self.graph, pos, node_size=250)
        nx.draw_networkx_edges(self.graph, pos, width=2)
        nx.draw_networkx_labels(self.graph, pos, labels={n: n + 1 for n in self.graph})

        self.canvas.draw()

    # Defining the function that will show the graph in the GUI
    def show_graph(self):

        self.create_canvas()

        if not self.vertex_entry.get().isnumeric() or not int(self.vertex_entry.get()) > 0:
            messagebox.showinfo(title="Error", message="Enter a valid number!")
            return

        self.size = int(self.vertex_entry.get())

        self.graph = self.create_graph()

        # We create the figures where the graph will be
        self.plot_graph()

    def color_graph(self):
        matrix = nx.to_numpy_array(self.graph)

        node = [str(x) for x in range(self.size)]
        t_ = {}
        for i in range(len(matrix)):
            t_[node[i]] = i

        degree = [sum(matrix[i]) for i in range(len(matrix))]

        # initiate the possible color
        color_dict = {}
        for i in range(len(matrix)):
            color_dict[node[i]] = ['#e6194b',
                                   '#3cb44b',
                                   '#ffe119',
                                   '#4363d8',
                                   '#f58231',
                                   '#911eb4',
                                   '#46f0f0',
                                   '#f032e6',
                                   '#bcf60c',
                                   '#fabebe',
                                   '#008080',
                                   '#e6beff',
                                   '#9a6324',
                                   '#fffac8',
                                   '#800000',
                                   '#aaffc3',
                                   '#808000',
                                   '#ffd8b1',
                                   '#000075',
                                   '#808080']

        # sort the node depends on the degree

        sorted_node = []
        index = []

        # use selection sort
        for i in range(len(degree)):
            _max = 0
            idx = 0
            for j in range(len(degree)):
                if j not in index:
                    if degree[j] >= _max:
                        _max = degree[j]
                        idx = j
            index.append(idx)
            sorted_node.append(node[idx])

        solution = {}

        for u in sorted_node:
            p = color_dict[u]
            for v in sorted_node:
                if matrix[int(u)][int(v)] == 1 and v in solution:
                    if solution[v] in p:
                        p.remove(solution[v])
            solution[u] = p[0]

        for key in solution.copy().keys():
            solution[int(key)] = solution.pop(key)

        sorted_solution = dict(sorted(solution.items()))

        for nodes, color in sorted_solution.items():
            self.colors.append(color)

        nx.draw_networkx_nodes(self.graph, self.pos, node_size=250, node_color=self.colors)
        nx.draw_networkx_edges(self.graph, self.pos, width=2)
        nx.draw_networkx_labels(self.graph, self.pos, labels={n: n + 1 for n in self.graph})
        self.canvas.draw()
        self.colors = []
