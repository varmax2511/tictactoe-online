'''
Created on Apr 21, 2018

An AI player will study the board, see the occupied cells by its pattern and
the opponent's pattern and then make a move

When the AI player makes a move, it should be propagated all the way the UI

@author: varunjai
'''
from com.varun.player.Player import Player


class AIPlayer(Player):

    def __init__(self, name: str, style: str):
        Player.__init__(self, name, style)
