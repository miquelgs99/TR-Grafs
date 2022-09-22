from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import GraphFrame
import SudokuColoringFrame
import SudokuFrame
import Main


class MenuFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        self.configure(bg_color="black")
        # self.configure(border_color="black")
        self.configure(border_width=2)

        # Buttons ----------
        nav_button1 = ctk.CTkButton(self,
                                    width=500,
                                    height=50,
                                    text_font=("helvetica", 14),
                                    border_width=1,
                                    corner_radius=8,
                                    border_color="black",
                                    text_color="black",
                                    text="El problema del camí més curt",
                                    command=lambda: self.new_window(GraphFrame.GraphFrame))
        nav_button1.grid(row=0, column=0, padx=10, pady=10)

        nav_button2 = ctk.CTkButton(self,
                                    width=500,
                                    height=50,
                                    text_font=("helvetica", 14),
                                    border_width=1,
                                    corner_radius=8,
                                    border_color="black",
                                    text_color="black",
                                    text="Coloració i resolució de sudokus",
                                    command=lambda: self.new_window(SudokuColoringFrame.SudokuColoringFrame))
        nav_button2.grid(row=1, column=0, padx=10, pady=10)

        nav_button3 = ctk.CTkButton(self,
                                    width=500,
                                    height=50,
                                    text_font=("helvetica", 14),
                                    border_width=1,
                                    corner_radius=8,
                                    border_color="black",
                                    text_color="black",
                                    text="Optimització d'una xarxa ferroviària",
                                    command=lambda: self.new_window(SudokuColoringFrame.SudokuColoringFrame))
        nav_button3.grid(row=2, column=0, padx=10, pady=10)
        # -------------------

