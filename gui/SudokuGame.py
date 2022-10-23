from SudokuMatrix import SudokuMatrix
import Main
import math
import networkx as nx
from pprint import pprint
import numpy as np


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

        def sorting(sol):
            sorted_node = []
            index = []
            degree = []
            for i in range(len(graph_matrix)):
                sum = 0
                for j in range(len(graph_matrix)):
                    if graph_matrix[i][j] == 1 and str(j) in sol:
                        sum += 1
                degree.append(sum)

            # use selection sort
            for _ in range(len(degree)):
                _max = 0
                idx = 0
                for j in range(len(degree)):
                    if j not in index:
                        if degree[j] >= _max:
                            _max = degree[j]
                            idx = j
                index.append(idx)
                sorted_node.append(node[idx])

            for element in sorted_node.copy():
                if str(element) in list(solution.keys()):
                    sorted_node.remove(element)
            return sorted_node

        solution = {}

        graph = nx.sudoku_graph()
        graph_matrix = nx.to_numpy_array(graph)

        for i in range(len(self.current_matrix)):
            for j in range(len(self.current_matrix)):
                if self.current_matrix[i][j] != 0:
                    solution[str((self.sudoku_size*i)+j)] = str(self.current_matrix[i][j])

        node = [str(x) for x in range(len(graph_matrix))]

        # initiate the possible color
        color_dict = {}
        for i in range(len(graph_matrix)):
            color_dict[node[i]] = ['1',
                                   '2',
                                   '3',
                                   '4',
                                   '5',
                                   '6',
                                   '7',
                                   '8',
                                   '9',
                                   '10',
                                   '11',
                                   '12',
                                   '13',
                                   '14',
                                   '15',
                                   '16',
                                   '17',
                                   '18',
                                   '19',
                                   '20']

        # sort the node depends on the degree
        sorted_nodes = sorting(solution)

        # algorithm
        # for u in sorted_node:
        #     if u in solution:
        #         break
        #     p = color_dict[u]
        #     for v in sorted_node:
        #         if graph_matrix[int(u)][int(v)] == 1 and v in solution:
        #             if solution[v] in p:
        #                 p.remove(solution[v])
        #
        #         print(p)
        #     solution[u] = p[0]
        iter_count = 0
        while True:
            u = sorted_nodes[0]
            p = color_dict[u]
            for v in solution:
                if graph_matrix[int(u)][int(v)] == 1 and v in solution:
                    if solution[v] in p:
                        p.remove(solution[v])

            # if len(p) == 1:
            #     iter_count = 0
            solution[u] = p[0]
            # else:
            #     iter_count += 1

            sorted_nodes = sorting(solution)

            count = 0
            for list_item in node:
                if list_item in solution:
                    count += 1

            if count == self.sudoku_size**2:
                break
            if iter_count > self.sudoku_size**2:
                break

        for key in solution.copy().keys():
            solution[int(key)] = solution.pop(key)

        sorted_solution = dict(sorted(solution.items()))

        for i in range(self.sudoku_size):
            for j in range(self.sudoku_size):
                self.current_matrix[i][j] = sorted_solution[(self.sudoku_size*i)+j]

        if 10 or 11 or 12 in sorted_solution.keys():
            Main.StdFrame.pop_error("PEDROOOOO", "Atenció", "L\'algorisme no ha pogut trobar una solució \n vàlida pel sudoku, així que ha utilitzat nombres més grans que nou per resoldre\'l.")
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
