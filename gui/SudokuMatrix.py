class SudokuMatrix(object):
    def __init__(self, size):
        self.sudoku_matrix = self.__create_empty_board(size)

    def __create_empty_board(self,size):
        board = []
        for i in range(0, size):
            board.append([])
            for j in range(0, size):
                board[i].append(0)
        return board
