import time
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import timeit
from SudokuGame import SudokuGame
import math
from tkinter import *
import Main


class EnterKeyValue:
    def __init__(self):
        self.last_clicked = timeit.default_timer()
        self.input_value = ""

    def enter_value(self, input_value, ):
        if timeit.default_timer() - self.last_clicked < 0.5:
            self.input_value += str(input_value)
        else:
            self.input_value = str(input_value)
            self.last_clicked = timeit.default_timer()


class SudokuFrame(Main.StdFrame):
    def __init__(self, root, sudoku_size):
        self.parent = root
        self.sudoku_size = sudoku_size
        self.set_size(sudoku_size=self.sudoku_size)
        # self.parent.title("Sudoku Frame")

        self.row = 0
        self.col = 0

        Frame.__init__(self, root)

        self.grid(column=0, row=0)

        self.create_frame = ttk.Frame(self, width=self.width, height=self.height)
        self.create_grid()

    def create_grid(self):
        self.create_frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.create_frame, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0, columnspan=self.sudoku_size, rowspan=self.sudoku_size)

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)
        self.canvas.bind("<BackSpace>", self.key_pressed)
        self.entry_key_value = EnterKeyValue()

        self.game = SudokuGame(sudoku_size=self.sudoku_size)
        self.game.start()

        self.draw_grid()

        submit_btn = ttk.Button(self.create_frame, text='Solve', command=self.solve_puzzle)
        submit_btn.grid(row=1, column=self.sudoku_size)

        clear = ttk.Button(self.create_frame, text='Clear', command=self.clear_frame)
        clear.grid(row=2, column=self.sudoku_size)

        change_sudoku_size = ttk.Entry(self.create_frame, width=6)
        change_sudoku_size.insert(0, self.sudoku_size)
        change_sudoku_size.bind("<Return>", (lambda event: self.set_sudoku_size(change_sudoku_size.get())))
        change_sudoku_size.grid(row=3, column=self.sudoku_size)

    def set_sudoku_size(self, size):
        size = int(size)
        if not math.sqrt(size).is_integer():
            tkMessageBox.showerror('La mida del sudoku és invàlida!',
                                   'Error: Ha de ser una potència.',
                                   parent=self.canvas)
        else:
            self.set_size(sudoku_size=size)
            self.create_frame.destroy()
            self.create_frame = ttk.Frame(self, width=self.width, height=self.height)
            self.create_grid()

    def set_size(self, sudoku_size=9):
        '''
        Calculates the dimension of the sudoku board.
        :param sudoku_size:
        :return:
        '''
        self.subgrid_size = math.sqrt(sudoku_size)
        self.sudoku_size = sudoku_size
        self.margin = 15
        self.side = 45
        self.width = self.margin * 2 + self.sudoku_size * self.side
        self.height = self.margin * 2 + self.sudoku_size * self.side

    def clear_frame(self):
        '''
        Function clears the frame
        :return:
        '''
        self.game.start()
        self.canvas.delete('numbers')

    def update_grid(self):
        self.canvas.delete("numbers")
        for i in range(self.sudoku_size):
            for j in range(self.sudoku_size):
                answer = self.game.current_matrix[i][j]
                if answer != 0:
                    x = self.margin + j * self.side + self.side / 2
                    y = self.margin + i * self.side + self.side / 2
                    original = self.game.initial_matrix[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)

    def draw_grid(self):
        for i in range(self.sudoku_size + 1):
            color = 'blue' if i % self.subgrid_size == 0 else 'gray'

            # vertical lines
            x0 = self.margin + i * self.side
            y0 = self.margin
            x1 = self.margin + i * self.side
            y1 = self.height - self.margin

            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            # horizontal lines
            x0 = self.margin
            y0 = self.margin + i * self.side
            x1 = self.width - self.margin
            y1 = self.margin + i * self.side

            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def cell_clicked(self, event):
        self.entry_key_value = EnterKeyValue()
        x, y = event.x, event.y
        if self.margin < x < self.width - self.margin and self.margin < y < self.height - self.margin:
            self.canvas.focus_set()

            row, col = int((y - self.margin) / self.side), int((x - self.margin) / self.side)

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.initial_matrix[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.draw_cursor()

    def key_pressed(self, event):
        if event.keysym== 'BackSpace':
            self.game.current_matrix[self.row][self.col] = 0
            self.update_grid()
            self.draw_cursor()
        elif self.row >= 0 and self.col >= 0 and event.char.isnumeric() and int(event.char) in list(
                range(0, self.sudoku_size)):
            self.entry_key_value.enter_value(event.char)
            if not self.game.is_valid(int(self.entry_key_value.input_value), self.row, self.col):
                tkMessageBox.showerror('Sudoku invàlid!',
                                       'Error: No es pot posar un ' + self.entry_key_value.input_value + ' en aquesta posició.',
                                       parent=self.canvas)
                return
            elif int(self.entry_key_value.input_value) > self.sudoku_size:
                tkMessageBox.showerror('Sudoku invàlid!',
                                       'Error: Els valors han de ser entre 1 i '+ str(self.sudoku_size),
                                       parent=self.canvas)
                return

            self.game.current_matrix[self.row][self.col] = int(self.entry_key_value.input_value)
            self.update_grid()
            self.draw_cursor()

    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = self.margin + self.col * self.side + 1
            y0 = self.margin + self.row * self.side + 1
            x1 = self.margin + (self.col + 1) * self.side - 1
            y1 = self.margin + (self.row + 1) * self.side - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", tags="cursor")

    def solve_puzzle(self):
        self.row, self.col = -1, -1
        if self.game.solve():
            self.update_grid()
        else:
            tkMessageBox.showerror('No solution!',
                                   'No s\'ha trobat solució',
                                   parent=self.canvas)


if __name__ == "__main__":
    root = Tk()
    SudokuFrame(root, 9)

    root.mainloop()
