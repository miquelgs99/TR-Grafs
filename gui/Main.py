from tkinter import *
from tkinter import ttk
import MenuFrame


class MainGui:

    def __init__(self):
        self.main_win = MenuFrame.MenuFrame()
        self.main_win.grid(row=0, column=0, padx=10, pady=10)

    def run_gui(self):
        self.main_win.mainloop()

    def refresh(self):
        self.destroy()
        self.__init__()


if __name__ == '__main__':
    mainGui = MainGui()
    mainGui.run_gui()
