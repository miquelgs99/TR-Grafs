from SudokuMatrix import SudokuMatrix
import math

class SudokuGame(object):
    def __init__(self, sudoku_size=9):
        self.initial_matrix = SudokuMatrix(sudoku_size).sudoku_matrix
        self.sudoku_size = sudoku_size
        self.subgrid_size = int(math.sqrt(self.sudoku_size))


    def start(self):
        self.current_matrix = []
        for i in range(self.sudoku_size):
            self.current_matrix.append([])
            for j in range(self.sudoku_size):
                self.current_matrix[i].append(self.initial_matrix[i][j])

    def solve(self):
        # Solve problem
        for i in range(0, self.sudoku_size):
            for j in range(0, self.sudoku_size):
                if self.current_matrix[i][j] == 0:
                    self.current_matrix[i][j] = -1
        return True

    def is_valid(self, num, row, col):
        # Check Row
        for i in range(self.sudoku_size):
            if self.current_matrix[row][i] == num and col != i:
                return False

        # Check Column
        for i in range(self.sudoku_size):
            if self.current_matrix[i][col] == num and row != i:
                return False

        # Check Box
        box_x = col // self.subgrid_size
        box_y = row // self.subgrid_size

        for i in range(box_y * self.subgrid_size, box_y * self.subgrid_size + self.subgrid_size):
            for j in range(box_x * self.subgrid_size, box_x * self.subgrid_size + self.subgrid_size):
                if self.current_matrix[i][j] == num and i != row and j != col:
                    return False
        return True
