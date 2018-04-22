'''
Created on Apr 19, 2018

@author: varunjai
'''
from com.varun.board.Piece import Piece


class Cell(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.piece = None
        
    def isoccupied(self):
        if(self.piece):
            return True
        return False
    
    def place(self, piece: Piece):
        self.piece = piece
    '''
    @return: can be None or the Piece class instance
    '''
    def getPiece(self):    
        return self.piece
