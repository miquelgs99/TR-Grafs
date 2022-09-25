import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from grave.style import use_attributes
from grave import plot_network


class MapCanvas(tk.Canvas):
    def get_image(self, f):
        img = Image.open(f)  # read the image file
        new_im_w = 890
        new_im_h = 555    # int(img.height / img.width * new_im_w)
        img = img.resize((new_im_w, new_im_h))  # new width & height
        self.line = None
        return ImageTk.PhotoImage(img)

    def __init__(self, root, f, frame):
        self.frame = frame
        self.image = self.get_image(f)
        super().__init__(master=root, width=self.image.width(), height=self.image.height())
        self.bind("<Button-1>", self.canvas_clicked)
        self.bind("<B1-Motion>", self.canvas_dragged)
        self.create_text(200, 250, text="Welcome")
        self.create_image(0, 0, image=self.image, anchor="nw")
        self.state = "scale"
        self.graph = nx.Graph()

        generate_button = ctk.CTkButton(self.frame,
                                        text="Generar graf!",
                                        text_font=("helvetica", 12),
                                        width=120,
                                        height=32,
                                        corner_radius=8,
                                        text_color="black",
                                        command=self.show_graph)
        generate_button.grid(column=0, row=2, padx=10, pady=10)

        self.vertex_entry = ctk.CTkEntry(self.frame, width=50)
        self.vertex_entry.grid(column=0, row=1, padx=10, pady=10)

    def canvas_clicked(self, event):
        if self.state == "scale":
            self.x1, self.y1 = event.x, event.y
            self.del_line()
            self.line = self.create_line(self.x1, self.y1, self.x1, self.y1, fill="black", width=20)

    def canvas_dragged(self, event):
        if self.state == "scale":
            self.x2, self.y2 = event.x, event.y
            if self.line:
                self.coords(self.line, self.x1, self.y1, self.x2, self.y2)

    def del_line(self):
        if self.line:
            self.delete(self.line)

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
        self.fig.set_figwidth(8.6)
        # self.fig.set_facecolor("#00000F")

        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(column=0, row=0, padx=20, pady=20, sticky="E")
        self.canvas.draw()

    # Defining the function that will create a graph from the entry
    def create_graph(self):

        graph = nx.random_tree(self.size)

        for node in graph.nodes:
            # graph.add_edge(node, np.random.randint(self.size - node - 1, self.size))
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

        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        pos = nx.shell_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=8)

        self.canvas.draw()

    # Defining the function that will show the graph in the GUI
    def show_graph(self):

        self.create_canvas()

        if not self.vertex_entry.get().isnumeric() or not int(self.vertex_entry.get()) > 0:
            # messagebox.showinfo(title="Error", message="Enter a valid number!")
            self.pop_error("Error", "Introdueix un nombre vàlid!")
            return

        self.size = int(self.vertex_entry.get())

        self.graph = self.create_graph()

        # We create the figures where the graph will be
        self.plot_graph()

    def pop_error(self, title, text):

        error = ctk.CTkToplevel(self)
        x = self.winfo_x()
        y = self.winfo_y()
        error.geometry("+%d+%d" % (x+720, y+300))
        error.overrideredirect(True)

        error_frame = ctk.CTkFrame(error, corner_radius=10, width=200, height=200, bg_color="white",
                                   border_width=2)
        error_frame.grid(column=0, row=0)

        error_frame.columnconfigure(0, weight=1)
        error_frame.rowconfigure(0, weight=2)

        error.wm_attributes('-transparentcolor', 'white')

        title_label = ctk.CTkLabel(error_frame, text=title, text_font=("bold helvetica", 25))
        title_label.grid(column=0, row=0, padx=20, pady=20)

        error_label = ctk.CTkLabel(error_frame, text=text, text_font=("helvetica", 12, "italic"))
        error_label.grid(column=0, row=1, padx=20, pady=10)

        quit_error = ctk.CTkButton(error_frame, text="D'acord",
                                   text_color="black", text_font=("helvetica", 12), command=error.destroy)
        quit_error.grid(column=0, row=2, pady=10)
