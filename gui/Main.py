from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import MenuFrame
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


class MainGui:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry('1280x720')
        self.root.resizable(False, False)
        self.root.title("Els grafs a la vida quotidiana: problemes i algorismes amb Python")

        self.image = Image.open("1.png")
        self.img_copy = self.image.copy()
        self.image = self.img_copy.resize((1280, 720))

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self.root, image=self.background_image)
        self.background.grid(column=0, row=0, sticky="nswe")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_win = MenuFrame.MenuFrame()
        main_win.grid(row=0, column=0, padx=10, pady=10)

        # region Menubar
        #
        # self.menubar = Menu(self.root)
        # self.root.config(menu=self.menubar)
        #
        # self.file_menu = Menu(self.menubar, tearoff=0)
        # self.edit_menu = Menu(self.menubar, tearoff=0)
        # self.help_menu = Menu(self.menubar, tearoff=0)
        #
        # self.menubar.add_cascade(label="Archivo", menu=self.file_menu)
        # self.menubar.add_cascade(label="Editar", menu=self.edit_menu)
        # self.menubar.add_cascade(label="Ayuda", menu=self.help_menu)
        #
        # self.file_menu.add_command(label="´Refresh", command=self.refresh)
        #
        # self.goto_menu = Menu(self.edit_menu, tearoff=0)
        # self.edit_menu.add_cascade(label="Go to", menu=self.goto_menu)
        # self.goto_menu.add_command(label='Menu', command=None)  # lambda: StdFrame.new_window(main_win, MenuFrame.MenuFrame
        # self.goto_menu.add_command(label='GraphFrame')
        # self.goto_menu.add_command(label='SudokuColoringFrame')
        #
        # self.help_menu.add_command(label="GitHub")
        # self.help_menu.add_command(label="FAQ")
        # self.file_menu.add_command(label="Quit")
        # endregion

    def run_gui(self):
        self.root.mainloop()

    def refresh(self):
        self.root.destroy()
        self.__init__()


class StdFrame(ctk.CTkFrame):

    def new_window(self, win):
        self.destroy()
        win = win()
        win.grid(row=0, column=0, padx=10, pady=10)
        win.mainloop()

    def __init__(self):
        ctk.CTkFrame.__init__(self)

    def pop_error(self, title, text):

        error = ctk.CTkToplevel(self)
        x = self.winfo_x()
        y = self.winfo_y()
        error.geometry("+%d+%d" % (x+720, y+300))
        error.overrideredirect(True)

        error_frame = ctk.CTkFrame(error, corner_radius=10, width=200, height=200, bg_color="white",
                                   border_width=2)
        error_frame.grid(column=0, row=0)

        error_frame.columnconfigure(0, weight=1)
        error_frame.rowconfigure(0, weight=2)

        error.wm_attributes('-transparent')

        title_label = ctk.CTkLabel(error_frame, text=title, text_font=("bold helvetica", 25))
        title_label.grid(column=0, row=0, padx=20, pady=20)

        error_label = ctk.CTkLabel(error_frame, text=text, text_font=("helvetica", 12, "italic"))
        error_label.grid(column=0, row=1, padx=20, pady=10)

        quit_error = ctk.CTkButton(error_frame, text="D'acord",
                                   text_color="black", text_font=("helvetica", 12), command=error.destroy)
        quit_error.grid(column=0, row=2, pady=10)


if __name__ == '__main__':
    mainGui = MainGui()
    mainGui.run_gui()
