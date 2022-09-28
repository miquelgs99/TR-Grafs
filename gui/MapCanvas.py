import customtkinter as tk
from tkinter import Frame
from PIL import Image, ImageTk
import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk

class MapCanvas(Frame):
    def __init__(self, root, f):
        self.image = self.get_image(f)

        super().__init__(root, bg="blue", width=self.image.width, height=self.image.height)

        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.image)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        plt.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(fill="both")
        self.canvas.get_tk_widget().config(width=self.image.width, height=self.image.height)

        self.fid1 = self.canvas.get_tk_widget().bind("<Button-1>", self.canvas_clicked)
        self.fid2 = self.canvas.get_tk_widget().bind("<B1-Motion>", self.canvas_dragged)
        self.canvas.draw()

        self.line = None

    def get_image(self, f):
        img = Image.open(f)  # read the image file
        new_im_w = 500
        new_im_h = int(img.height / img.width * new_im_w)
        img = img.resize((new_im_w, new_im_h))  # new width & height
        return img

    def canvas_clicked(self, event):
        self.x1, self.y1 = event.x, event.y
        self.del_line()
        self.line = self.canvas.get_tk_widget().create_line(self.x1, self.y1, self.x1, self.y1, fill="black", width=20)

    def point_clicked(self, event):
        x = event.x  # x coordinate of event, not Data
        y = event.y  # y coordinate of event, not Data
        self.ax.plot(x, y, 'ro')
        self.canvas.draw()

    def canvas_dragged(self, event):
        self.x2, self.y2 = event.x, event.y
        if self.line:
            self.canvas.get_tk_widget().coords(self.line, self.x1, self.y1, self.x2, self.y2)

    def del_line(self):
        if self.line:
            self.canvas.get_tk_widget().delete(self.line)

    def change_add_points(self):
        if self.fid1:
            self.canvas.get_tk_widget().unbind("<Button-1>", self.fid1)
            self.canvas.get_tk_widget().unbind("<B1-Motion>", self.fid2)
        self.canvas.get_tk_widget().bind("<Button-1>", self.point_clicked)
