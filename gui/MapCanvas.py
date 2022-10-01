import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from grave.style import use_attributes
from grave import plot_network
import math


class MapCanvas(ctk.CTkFrame):
    def __init__(self, root, f, text_frame):

        self.text_frame = text_frame
        self.image = self.get_image(f)
        super().__init__(root, bg="blue")
        self.node_counter = 0
        self.positions = {}
        self.unit_distance = 0
        self.scale = 0

        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.image)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(sticky="nswe")
        self.canvas.get_tk_widget().config(width=self.image.width, height=self.image.height)

        self.fid1 = self.canvas.get_tk_widget().bind("<Button-1>", self.canvas_clicked)
        self.fid2 = self.canvas.get_tk_widget().bind("<B1-Motion>", self.canvas_dragged)
        self.canvas.draw()
        self.line = None

        self.graph = nx.Graph()

    @staticmethod
    def get_image(f):
        img = Image.open(f)  # read the image file
        new_im_w = 500
        new_im_h = int(img.height / img.width * new_im_w)
        img = img.resize((new_im_w, new_im_h))  # new width & height
        return img

    def point_clicked(self, event):
        x = event.x  # x coordinate of event, not Data
        y = event.y  # y coordinate of event, not Data
        self.ax.plot(x, y, 'ro')
        self.node_counter += 1
        self.positions[self.node_counter] = (x, y)
        # self.G.add_node(self.node_counter, pos=(x, y))
        self.canvas.draw()

    def canvas_clicked(self, event):
        self.x1, self.y1 = event.x, event.y
        self.del_line()
        self.line = self.canvas.get_tk_widget().create_line(self.x1, self.y1, self.x1, self.y1, fill="black",
                                                            width=10)

    def canvas_dragged(self, event):
        self.x2, self.y2 = event.x, event.y
        if self.line:
            self.unit_distance = round(self.calculate_distance(self.x1, self.y1, self.x2, self.y2))
            self.canvas.get_tk_widget().coords(self.line, self.x1, self.y1, self.x2, self.y2)

    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def del_line(self):
        if self.line:
            self.canvas.get_tk_widget().delete(self.line)

    def change_add_points(self):
        if self.fid1:
            self.canvas.get_tk_widget().unbind("<Button-1>", self.fid1)
            self.canvas.get_tk_widget().unbind("<B1-Motion>", self.fid2)
        self.canvas.get_tk_widget().bind("<Button-1>", self.point_clicked)

    def draw_graph(self):
        self.graph.add_nodes_from(self.positions.keys())
        self.graph.add_edges_from((u, v) for u in self.graph.nodes() for v in self.graph.nodes() if u != v)
        for n, p in self.positions.items():
            self.graph.nodes[n]['pos'] = p

        for u, v, attr in self.graph.edges(data=True):
            node1_x = self.graph.nodes[u]["pos"][0]
            node1_y = self.graph.nodes[u]["pos"][1]
            node2_x = self.graph.nodes[v]["pos"][0]
            node2_y = self.graph.nodes[v]["pos"][1]

            node_dist = round(self.calculate_distance(node1_x, node1_y, node2_x, node2_y))

            attr["weight"] = int(round((node_dist/self.unit_distance), 2) * int(self.scale))

        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw(self.graph, pos=self.positions)
        nx.draw_networkx_edge_labels(self.graph, pos=self.positions, edge_labels=edge_labels)
        self.canvas.draw()

