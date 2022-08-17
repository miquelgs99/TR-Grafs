from tkinter import *
from tkinter import ttk
import MenuFrame


class MainGui:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('1300x900')

        # region Menubar

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.edit_menu = Menu(self.menubar, tearoff=0)
        self.help_menu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Archivo", menu=self.file_menu)
        self.menubar.add_cascade(label="Editar", menu=self.edit_menu)
        self.menubar.add_cascade(label="Ayuda", menu=self.help_menu)

        self.file_menu.add_command(label="´Refresh", command=self.refresh)
        self.edit_menu.add_command(label="Go to")

        self.help_menu.add_command(label="GitHub")
        self.help_menu.add_command(label="FAQ")
        self.file_menu.add_command(label="Quit")
        # endregion

        main_win = MenuFrame.MenuFrame()
        main_win.grid(row=0, column=0, padx=10, pady=10)

    def run_gui(self):
        self.root.mainloop()

    def refresh(self):
        self.root.destroy()
        self.__init__()


if __name__ == '__main__':
    mainGui = MainGui()
    mainGui.run_gui()
