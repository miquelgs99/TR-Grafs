from tkinter import *
from tkinter import ttk
import MenuFrame


root = Tk()
root.geometry('1280x720')
main_win = MenuFrame.MenuFrame()
main_win.grid(row=0, column=0, padx=10, pady=10)
root.mainloop()
