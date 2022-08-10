from tkinter import *
from tkinter import ttk
import control
import GraphFrame
import MenuFrame

class SummaryFrame(control.StdFrame):

    def __init__(self):
        control.StdFrame.__init__(self)

        nav_button1 = ttk.Button(self, text="MenuFrame",
                                 command=lambda: self.new_window(MenuFrame.MenuFrame))
        nav_button1.grid(row=0, column=0)

        nav_button2 = ttk.Button(self, text="GraphFrame",
                                 command=lambda: self.new_window(GraphFrame.GraphFrame))
        nav_button2.grid(row=0, column=1)

        quit_button = ttk.Button(self, text="Quit",
                                 command=lambda: self.destroy())
        quit_button.grid(row=0, column=2)
