'''
Created on Apr 21, 2018

An AI player will study the board, see the occupied cells by its pattern and
the opponent's pattern and then make a move

When the AI player makes a move, it should be propagated all the way the UI

@author: varunjai
'''
import random
from com.varun.player.Player import Player
from com.varun.game.Game import Game

class AIMoveParam(object):
    def __init__(self, xval: int, yval: int, style: str):
        self.xval = xval
        self.yval = yval
        self.style = style
        
    def getXval(self):
        return self.xval
    
    def getYval(self):
        return self.yval
    
    def getStyle(self):
        return self.style    
    
class AIPlayer(Player):

    def __init__(self, name: str, style: str, game: Game):
        Player.__init__(self, name, style)
        self.game = game

    def move(self):
        # write a dump policy for now
        # find first unoccupied cell and mark it
        cells = self.game.get_empty_cells()
        if(cells is None):
            return None
        
        cell = cells[random.randint(0, len(cells) - 1)]
        
        if(cell is None):
            return None
        
        return AIMoveParam(cell.xval(), cell.yval(), self.style)
        