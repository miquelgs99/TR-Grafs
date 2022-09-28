import MapCanvas
import Main
import customtkinter as ctk

import tkinter as tk
import MenuFrame

class MapFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        subFrame1 = ctk.CTkFrame(self, corner_radius=0, width=20)
        subFrame1.grid(row=0, column=0)
        l1 = ctk.CTkLabel(subFrame1, text='Escull un mapa com a fons.', width=30)
        l1.grid(row=0, column=0)
        b1 = ctk.CTkButton(subFrame1, text='Upload Files', width=20, command=self.upload_file)
        b1.grid(row=0, column=1)
        b2 = ctk.CTkButton(subFrame1, text='Escollir punts', width=20, command=self.choose_points)
        b2.grid(row=0, column=2)
        b3 = ctk.CTkButton(subFrame1, text='Imprimir graf', width=20, command=self.imprimir_mapa)
        b3.grid(row=0, column=3)

        # creates a frame that is a child of 'mainFrame'
        subFrame2 = ctk.CTkFrame(self)
        subFrame2.grid(row=1, column=0)
        l2 = ctk.CTkLabel(subFrame2, text='Escala', width=8)
        l2.grid(row=1, column=0)
        self.b2 = ctk.CTkLabel(subFrame2, text=' : ', width=7)
        self.b2.grid(row=1, column=1)
        l3 = ctk.CTkLabel(subFrame2, text='Introdueix distància:', width=20)
        l3.grid(row=1, column=2)
        e1 = ctk.CTkEntry(subFrame2, width=5)
        e1.bind("<Return>", (lambda event: self.reply(e1.get())))
        e1.grid(row=1, column=3)

    def reply(self, name):
        self.b2.config(text="1:" + name)

    def upload_file(self):
        f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'), ('PNG Files', '*.png')]
        f = tk.filedialog.askopenfilename(filetypes=f_types)
        subFrame3 = ctk.CTkFrame(self)
        subFrame3.grid(row=2, column=0)
        self.mapCanvas = MapCanvas.MapCanvas(self, f)
        self.mapCanvas.grid(row=2, column=0)

    def choose_points(self):
        if self.mapCanvas:
            self.mapCanvas.change_add_points()

    def imprimir_mapa(self):
        if self.mapCanvas:
            self.mapCanvas.draw_graph()


if __name__ == "__main__":
    app = MapFrame()
    app.mainloop()
