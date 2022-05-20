from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("500x500")

mainframe = ttk.Frame(root, padding = 5, borderwidth = 100, relief = "ridge")
mainframe.grid()

root.minsize(500, 500)
root.maxsize(500, 500)

root.mainloop()