from tkinter import *
from tkinter import ttk
import GraphFrame
import SummaryFrame
import control


class MenuFrame(control.StdFrame):

    def __init__(self):
        control.StdFrame.__init__(self)

        # Buttons ----------
        nav_button1 = ttk.Button(self, text="GraphFrame",
                                 command=lambda: self.new_window(GraphFrame.GraphFrame))
        nav_button1.grid(row=0, column=0, sticky=W)

        nav_button2 = ttk.Button(self, text="SummaryFrame",
                                 command=lambda: self.new_window(SummaryFrame.SummaryFrame))
        nav_button2.grid(row=1, column=0, sticky=E)
        # -------------------

