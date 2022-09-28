import tkinter as tk
from tkinter import filedialog
import MapCanvas
import Main


class MapFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)

        self.image = None
        self.image2 = None
        # self.geometry("600x600")  # Size of the window
        # self.title('Xarxa ferroviària')
        my_font1 = ('times', 18, 'bold')

        subFrame1 = tk.Frame(self)
        subFrame1.grid(row=0, column=0)
        l1 = tk.Label(subFrame1, text='Escull un mapa com a fons.', width=30, font=my_font1)
        l1.grid(row=0, column=0)
        b1 = tk.Button(subFrame1, text='Upload Files', width=20, command=self.upload_file)
        b1.grid(row=0, column=1)
        b2 = tk.Button(subFrame1, text='Escollir punts', width=20, command=self.choose_points)
        b2.grid(row=0, column=2)

        # creates a frame that is a child of 'mainFrame'
        subFrame2 = tk.Frame(self)
        subFrame2.grid(row=1, column=0)
        l2 = tk.Label(subFrame2, text='Escala', width=8, font=my_font1)
        l2.grid(row=1, column=0)
        self.b2 = tk.Label(subFrame2, text=' : ', width=7, font=my_font1)
        self.b2.grid(row=1, column=1)
        l3 = tk.Label(subFrame2, text='Introdueix distància:', width=20, font=my_font1)
        l3.grid(row=1, column=2)
        e1 = tk.Entry(subFrame2, width=5)
        e1.bind("<Return>", (lambda event: self.reply(e1.get())))
        e1.grid(row=1, column=3)

    def reply(self, name):
        self.b2.config(text="1:" + name)

    def upload_file(self):
        f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'), ('PNG Files', '*.png')]
        f = tk.filedialog.askopenfilename(filetypes=f_types)
        subFrame3 = tk.Frame(self)
        subFrame3.grid(row=2, column=0)
        self.mapCanvas = MapCanvas.MapCanvas(self, f)
        self.mapCanvas.grid(row=2, column=0)

    def choose_points(self):
        if self.mapCanvas:
            self.mapCanvas.change_add_points()


if __name__ == "__main__":
    app = MapFrame()
    app.mainloop()
