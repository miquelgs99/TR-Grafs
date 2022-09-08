import tkinter as tk
from PIL import Image, ImageTk


class MapCanvas(tk.Canvas):
    def get_image(self, f):
        img = Image.open(f)  # read the image file
        new_im_w = 500
        new_im_h = int(img.height / img.width * new_im_w)
        img = img.resize((new_im_w, new_im_h))  # new width & height
        self.line = None
        return ImageTk.PhotoImage(img)

    def __init__(self, root, f):
        self.image = self.get_image(f)
        super().__init__(master=root, width=self.image.width(), height=self.image.height())
        self.bind("<Button-1>", self.canvas_clicked)
        self.bind("<B1-Motion>", self.canvas_dragged)
        self.create_text(200, 250, text="Welcome")
        self.create_image(0, 0, image=self.image, anchor="nw")

    def canvas_clicked(self, event):
        self.x1, self.y1 = event.x, event.y
        self.del_line()
        self.line = self.create_line(self.x1, self.y1, self.x1, self.y1, fill="black", width=20)

    def canvas_dragged(self, event):
        self.x2, self.y2 = event.x, event.y
        if self.line:
            self.coords(self.line, self.x1, self.y1, self.x2, self.y2)

    def del_line(self):
        if self.line:
            self.delete(self.line)


