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


class SudokuColoringFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        # self.configure(width=1180, height=710)
        self.grid(sticky="nswe")

        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        self.size = 0
        self.graph = nx.Graph()

        text_frame = ctk.CTkFrame(self, corner_radius=0)
        text_frame.grid(column=0, row=0, sticky="nswe", rowspan=2)

        top_text_frame = ctk.CTkFrame(self)
        top_text_frame.grid(column=1, row=0)

        self.sudoku_frame = SudokuFrame.SudokuFrame(self, 9)
        self.sudoku_frame.grid(column=1, row=1, sticky="nswe")
        self.coloring_frame = ctk.CTkFrame(self)
        self.coloring_frame.grid(column=1, row=1, sticky="nswe")

        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(column=1, row=1, padx=20, sticky="E")

        self.create_canvas()

        # region We create the entry text box

        vertex_label = ctk.CTkLabel(text_frame, text="Quants vèrtexs tindrà el graf?", text_font=("helvetica", 12))
        vertex_label.grid(column=0, row=0, padx=10, pady=10)

        self.vertex_entry = ctk.CTkEntry(text_frame, width=50)
        self.vertex_entry.grid(column=0, row=1, padx=10, pady=10)
        # endregion

        self.which_frame = "Coloring"

        self.left_label = ctk.CTkLabel(top_text_frame,
                                       text='Coloring',
                                       text_color="#383838",
                                       text_font=('Segoe UI', 15))
        self.left_label.grid(column=0, row=0, padx=20)

        self.mid_label = ctk.CTkLabel(top_text_frame,
                                      text='Coloring',
                                      text_font=('Segoe UI', 20))
        self.mid_label.grid(column=1, row=0, padx=20)

        self.right_label = ctk.CTkLabel(top_text_frame,
                                        text='Sudoku',
                                        text_font=('Segoe UI', 15))
        self.right_label.grid(column=2, row=0, padx=20)

        top_text_frame.bind("<Return>", lambda event, btn="left": self.change_to(btn))
        # self.right_label.bind("<Button-1>", lambda event, btn="right": self.change_to(btn))

        # region Creating the buttons

        # We create the button that will generate the graph, and we assign the previous function made to it
        generate_button = ctk.CTkButton(text_frame,
                                        text="Generate!",
                                        text_font=("helvetica", 12),
                                        width=120,
                                        height=32,
                                        corner_radius=8,
                                        text_color="black",
                                        command=self.show_graph)
        generate_button.grid(column=0, row=2, padx=10, pady=10)

        # We create the button that will create the random number, and we assign the previous function made to it
        random_button = ctk.CTkButton(text_frame,
                                      text="Random number!",
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
        random_button.grid(column=0, row=3, padx=10, pady=10)

        nav_button1 = ctk.CTkButton(nav_frame,
                                    text="MenuFrame",
                                    width=120,
                                    height=32,
                                    corner_radius=8,
                                    text_color="black",
                                    command=lambda: self.new_window(MenuFrame.MenuFrame))
        nav_button1.grid(row=0, column=0)

        # endregion

    def change_to(self, btn, event=None):

        if self.which_frame == "Coloring" and btn == "right":
            self.left_label.configure(foreground='black')
            self.mid_label.configure(text='Sudoku')
            self.right_label.configure(foreground='#383838')
            self.which_frame = "Sudoku"

            self.sudoku_frame.tkraise()

        elif self.which_frame == "Sudoku" and btn == "left":
            self.left_label.configure(foreground='#383838')
            self.mid_label.configure(text='Coloring')
            self.right_label.configure(foreground='black')
            self.which_frame = "Coloring"

            self.coloring_frame.tkraise()

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
        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.coloring_frame)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(column=0, row=0, padx=20, pady=20)
        self.canvas.draw()

    def create_graph(self):
        # The matrix of the graph is created with randint from numpy
        matrix = np.random.randint(-4, 2, size=(self.size, self.size))

        isolated_node = 0

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):

                if matrix[i][j] != matrix[j][i]:
                    matrix[i][j] = matrix[j][i]

                if matrix[i][j] < 0:
                    matrix[i][j] = 0

                if matrix[i][j] == 0:
                    isolated_node += 1

            if isolated_node == len(matrix):
                rep = (np.random.randint(1, len(matrix)))
                for _ in range(rep):
                    # try:
                    #     matrix[i][i+1] = 1
                    # except IndexError:
                    #     matrix[i][i-1] = 1
                    matrix[i][np.random.randint(0, (len(matrix)))] = 1
            isolated_node = 0
            matrix[i][i] = 0

        # We create the graph from the matrix
        return nx.from_numpy_matrix(matrix)

    # Defining the function that will plot the graph in matplotlib
    def plot_graph(self):

        for node, node_attr in self.graph.nodes(data=True):
            node_attr['size'] = 500

        art = plot_network(self.graph, layout="spring", ax=self.ax,
                           node_style=use_attributes(),
                           edge_style=use_attributes(),
                           node_label_style={'font_size': 7,
                                             'font_weight': 'bold',
                                             'font_color': 'k',
                                             'bbox': {'alpha': 0}
                                             })

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
