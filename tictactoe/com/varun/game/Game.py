'''
Created on Apr 19, 2018

@author: varunjai
'''
from test.test_funcattrs import empty_cell

from com.varun.board.Board import Board
from com.varun.board.Piece import Piece
from com.varun.game.PlayerData import PlayerData


class Game(object):

    def __init__(self, player1: PlayerData, player2: PlayerData, n: int):
        self.players = [player1, player2]
        self.board = Board(n)
        self.current_player_idx = 0

    def move(self, x: int, y: int):

        val = self.board.place_cell(Piece(self.get_current_player().get_player_style()), x, y)
        if(val is None):
            return ''

        # change current player
        self.__toggle_player()

        return val

    def __set_current_player(self, player: PlayerData):
        self.current_player = player

    def __toggle_player(self):
        # change current player
        self.current_player_idx = len(self.players) - self.current_player_idx - 1

    def checkGame(self):
        if(self.board.isWin()):
            return 'win'

        if(self.board.isBoardFull()):
            return 'tie'

        # game is not yet over
        return ''

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def get_empty_cells(self):
        return self.board.get_empty_cells()
        