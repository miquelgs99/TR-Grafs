from tkinter import *
from tkinter import ttk
import time
import os.path
import os
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import graph_generator

def GenerarGrafo(*args):
    plt.cla()
    graph_generator.grafo()

root = Tk()
root.title("TR-Grafs")
root.geometry('660x750')
#root.resizable(0, 0)

mainframe = ttk.Frame(root)
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
mainframe.columnconfigure(0, weight=2)
mainframe.rowconfigure(0, weight=2)

NumOfV = StringVar()

MainEntry = ttk.Entry(mainframe, textvariable=NumOfV, width = 15)
MainEntry.grid(column = 1, row = 0, padx = 20, pady = 20)

GenerateButton = ttk.Button(mainframe, text="Generate!", command=GenerarGrafo)
GenerateButton.grid(column = 1, row = 1)

# Creem la direcció de la imatge que guardarem sempre a la carpeta de imatges situada en la carpeta pare de l'actual.

my_file = "figure.jpg"
image_path = os.path.join(os.path.join(os.path.pardir,graph_generator.PATH_IMAGES), my_file)
Img = ImageTk.PhotoImage(Image.open(image_path))
ImgLabel = ttk.Label(mainframe, image=Img)
ImgLabel.grid(column=1, row=3, padx=10)


#for child in mainframe.winfo_children():
 #   child.grid_configure(padx=5, pady=5)

root.bind("<Return>", GenerarGrafo)
MainEntry.focus()
root.mainloop()
