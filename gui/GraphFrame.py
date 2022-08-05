from tkinter import *
from tkinter import ttk
import SummaryFrame
import control
import MenuFrame


class GraphFrame(control.StdFrame):

    def __init__(self):
        control.StdFrame.__init__(self)

        text_frame = ttk.Frame(self)
        text_frame.grid(column=0, row=0)

        # We create the frame where the graphs will be shown
        graph_frame = ttk.Frame(self)
        graph_frame.grid(column=1, row=0)

        # We put some text explaining what to write in the text box
        vertex_label = ttk.Label(text_frame, text="Introduce the number of vertex that you want: ")
        vertex_label.grid(column=0, row=0, padx=20, pady=20)

        # We create the entry text box
        vertex_entry = ttk.Entry(text_frame, width=15)
        vertex_entry.grid(column=1, row=0, padx=0, pady=20)




        nav_button1 = ttk.Button(self, text="SummaryFrame",
                                 command=lambda: self.new_window(SummaryFrame.SummaryFrame))
        nav_button1.grid(row=1, column=0)

        nav_button2 = ttk.Button(self, text="MenuFrame",
                                 command=lambda: self.new_window(MenuFrame.MenuFrame))
        nav_button2.grid(row=1, column=1)

