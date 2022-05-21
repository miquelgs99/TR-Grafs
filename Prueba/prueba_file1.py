from tkinter import *
from tkinter import ttk
import time
import os.path
import os

import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import prueba_file2

def split(*args):
    ExitText.set(" ".join(str(InitText.get())))
    print(ExitText.get())

def GenerarGrafo(*args):
    plt.cla()
    prueba_file2.Grafo()
    print("Imagen puesta")


root = Tk()
root.title("Splitter")
root.geometry('660x750')
#root.resizable(0, 0)

mainframe = ttk.Frame(root)
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
mainframe.columnconfigure(0, weight=2)
mainframe.rowconfigure(0, weight=2)

InitText = StringVar()
ExitText = StringVar()

MainEntry = ttk.Entry(mainframe, textvariable=InitText, width = 15)
MainEntry.grid(column = 1, row = 0, padx = 20, pady = 20)

SplitButton = ttk.Button(mainframe, text = "Split!", command = split)

SplitButton.grid(column = 1, row = 1)

ExitLabel = ttk.Label(mainframe, textvariable=ExitText, background = 'White', width = -15, relief = "ridge")
ExitLabel.grid(column = 1, row = 2, padx = 20, pady = 20)

# Creem la direcció de la imatge que guardarem sempre a la carpeta de imatges situada en la carpeta pare de l'actual.

my_file = "white.jpg"
image_path = os.path.join(os.path.join(os.path.pardir,prueba_file2.PATH_IMAGES), my_file)
Img = ImageTk.PhotoImage(Image.open(image_path))
ImgLabel = ttk.Label(mainframe, image=Img)
ImgLabel.grid(column=1, row=3, padx=10)


#for child in mainframe.winfo_children():
 #   child.grid_configure(padx=5, pady=5)

root.bind("<Return>", GenerarGrafo)
MainEntry.focus()
root.mainloop()
print("Hola que tal")
