from tkinter import *
from tkinter import ttk
from GraphFrame import *

class MenuFrame(Frame):

    def new_window(self):
        self.destroy()
        graph_frame = GraphFrame()
        graph_frame.grid(row=0, column=0)
        graph_frame.mainloop()

    def __init__(self):
        Frame.__init__(self)

        button = ttk.Button(self, text="Hello", command=lambda: self.new_window())
        button.grid(row=0, column=0)


