import tkinter as tk
import MapCanvas
import Main
import customtkinter as ctk
import MenuFrame


class MapFrame(Main.StdFrame):

    def __init__(self):
        Main.StdFrame.__init__(self)
        self.grid(sticky="nswe")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.image = None
        self.image2 = None
        my_font1 = ('Helvetica', 12)

        self.text_frame = ctk.CTkFrame(self, corner_radius=0, width=20)
        self.text_frame.grid(column=0, row=0, sticky="nswe", rowspan=2)
        self.text_frame.rowconfigure(0, weight=15)
        self.text_frame.rowconfigure(1, weight=1)
        self.text_frame.rowconfigure(2, weight=1)
        self.text_frame.rowconfigure(3, weight=1)
        self.text_frame.rowconfigure(4, weight=100)
        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.columnconfigure(1, weight=1)

        self.map_frame = ctk.CTkFrame(self, width=980, height=600)
        self.map_frame.grid(column=1, row=0, padx=10, pady=10, sticky="w")
        self.map_frame.grid_propagate(0)
        self.map_frame.columnconfigure(0, weight=1)
        self.map_frame.rowconfigure(0, weight=1)

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(column=1, row=1, padx=20, pady=10, sticky="we")
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)

        select_map = ctk.CTkButton(bottom_frame,
                                   text='Escollir mapa com a fons',
                                   text_font=("helvetica", 12),
                                   width=120,
                                   height=32,
                                   corner_radius=8,
                                   text_color="black",
                                   command=self.upload_file)
        select_map.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # creates a frame th
        scale_label = ctk.CTkLabel(bottom_frame, text='Escala: ', text_font=my_font1, anchor="e")
        scale_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.scale_value = ctk.CTkLabel(bottom_frame, text="", text_font=my_font1, anchor="w")
        self.scale_value.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        distance_label = ctk.CTkLabel(self.text_frame, text='Introdueix\n la distància que \n tindrà l\'escala:',
                                      text_font=my_font1, anchor="e")
        distance_label.grid(row=0, column=0, padx=10, sticky="e")

        scale_entry = ctk.CTkEntry(self.text_frame, width=50)
        scale_entry.bind("<Return>", (lambda event: self.reply(scale_entry.get())))
        scale_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        choose_button = ctk.CTkButton(self.text_frame,
                                      text='Escollir punts',
                                      text_font=("helvetica", 12),
                                      width=120,
                                      height=32,
                                      corner_radius=8,
                                      text_color="black",
                                      command=self.choose_points)
        choose_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        print_graph_button = ctk.CTkButton(self.text_frame,
                                           text='Imprimir graf',
                                           text_font=("helvetica", 12),
                                           width=120,
                                           height=32,
                                           corner_radius=8,
                                           text_color="black",
                                           command=self.print_graph)
        print_graph_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        find_tree_button = ctk.CTkButton(self.text_frame,
                                           text='Optimitzar graf',
                                           text_font=("helvetica", 12),
                                           width=120,
                                           height=32,
                                           corner_radius=8,
                                           text_color="black",
                                           command=self.find_tree)
        find_tree_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        go_to_menu = ctk.CTkButton(bottom_frame,
                                   text="Menú principal",
                                   width=120,
                                   height=32,
                                   corner_radius=8,
                                   text_color="black",
                                   command=lambda: self.new_window(MenuFrame.MenuFrame))
        go_to_menu.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    def reply(self, num):
        self.scale_value.configure(text="1:" + num)
        if self.mapCanvas:
            self.mapCanvas.scale = num

    def upload_file(self):
        f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'), ('PNG Files', '*.png')]
        f = tk.filedialog.askopenfilename(filetypes=f_types)
        self.mapCanvas = MapCanvas.MapCanvas(self.map_frame, f, self.text_frame)
        self.mapCanvas.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

    def choose_points(self):
        if self.mapCanvas:
            self.mapCanvas.change_add_points()

    def print_graph(self):
        if self.mapCanvas:
            self.mapCanvas.draw_graph(self.mapCanvas.graph.edges())

    def find_tree(self):
        self.mapCanvas.find_tree()


# if __name__ == "__main__":
#     app = MapFrame()
#     app.mainloop()
