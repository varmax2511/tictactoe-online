'''
Created on Apr 19, 2018

@author: varunjai
'''
from numpy import array
import numpy as np
from com.varun.board.Cell import Cell
from com.varun.board.Piece import Piece


class Board(object):

    def __init__(self, n):
        # create a multi-dimensional array of cells
        self.cells = [[Cell(i, j) for i in range(n)] for j in range(n)]

    def place_cell(self, piece: Piece, x: int, y: int):
        if(self.isCellOccupied(x, y)):
            return None

        self.cells[x][y].place(piece)
        return piece.get_style()

    '''
    Returns if the cell on the board is occupied or not
    '''

    def isCellOccupied(self, x: int, y: int):
        if(self.cells[x][y].isoccupied()):
            return True

        return False

    def isBoardFull(self):
        return all(all(cell.isoccupied() for cell in row) for row in self.cells)

    def isWin(self):
        # if any row is of all same style
        #  if(all((self.cells[j][0].getPiece().get_style() == self.cells[j][i].getPiece().get_style()
        #           for i in len(self.cells[j])) for j in len(self.cells))):

        for i in range(len(self.cells)):
            start = self.cells[i][0]

            # if row start is empty
            if(start.getPiece() is None):
                continue

            if(all(self.cells[i][j].getPiece() is not None and start.getPiece().get_style() == self.cells[i][j].getPiece().get_style()
                   for j in range(len(self.cells[i])))):
                return True

        # if any column is of all same style
        # if(all(self.cells[0][i].getPiece().get_style() == self.cells[j][i].getPiece().get_style()
        #    for i in range(i + 1)) for j in range(len(self.cells))):
        #    return True

        for i in range(len(self.cells)):
            start = self.cells[0][i]

            # if column start is empty
            if(start.getPiece() is None):
                continue

            if(all(self.cells[j][i].getPiece() is not None and start.getPiece().get_style() == self.cells[j][i].getPiece().get_style()
                   for j in range(len(self.cells[i])))):
                return True

        # if any diagonal is same
        matrix = array(self.cells)

        for i in range(2):
            diagonal = None
            if(i == 0):
                diagonal = matrix.diagonal(i)
            else:
                diagonal = np.diag(np.rot90(matrix))

            # if diagonal start is empty
            if(diagonal[0].getPiece() is None):
                continue

            if(all(diagonal[j].getPiece() is not None and diagonal[0].getPiece().get_style() == diagonal[j].getPiece().get_style() for j in range(1, len(diagonal)))):
                return True

            '''
            for j in range(1, len(diagonal)):
                if(diagonal[j].getPiece() is None or diagonal[0].getPiece().get_style() != diagonal[j].getPiece().get_style()):
                    return False

            # a diagonal is complete
            return True
            '''
        return False

