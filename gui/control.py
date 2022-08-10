from tkinter import *
from tkinter import ttk


class StdFrame(Frame):

    def new_window(self, win):
        self.destroy()
        win = win()
        win.grid(row=0, column=0, padx=10, pady=10)
        win.mainloop()

    def __init__(self):
        Frame.__init__(self)
        pass
