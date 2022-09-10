from tkinter import *
from tkinter import ttk
import GraphFrame
import SummaryFrame
import MapFrame
import Main


class MenuFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        # Buttons ----------
        nav_button1 = ttk.Button(self, text="GraphFrame",
                                 command=lambda: self.new_window(GraphFrame.GraphFrame))
        nav_button1.grid(row=0, column=0, sticky=W)

        nav_button3 = ttk.Button(self, text="MapFrame",
                                command=lambda: self.new_window(MapFrame.MapFrame))
        nav_button3.grid(row=1, column=0, sticky=E)

        nav_button2 = ttk.Button(self, text="SummaryFrame",
                                 command=lambda: self.new_window(SummaryFrame.SummaryFrame))
        nav_button2.grid(row=2, column=0, sticky=E)

        # -------------------


