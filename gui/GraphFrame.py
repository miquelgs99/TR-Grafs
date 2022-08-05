from tkinter import *
from tkinter import ttk


class GraphFrame(Frame):

    def __init__(self):
        Frame.__init__(self)
        quit_button = ttk.Button(self, text="Quit", command=lambda: self.destroy())
        quit_button.grid(row=0, column=0)


