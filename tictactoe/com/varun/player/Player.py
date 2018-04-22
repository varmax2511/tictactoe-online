'''
Created on Apr 19, 2018

A player will have its associated style like X or O
A player will be able to perform action to put a piece on the board
When performing an action, a piece instance will be created and placed
on the board

@author: varunjai
'''
from abc import ABC

class Player(ABC):
    
    def __init__(self, name, style):
        if(name is None or style is None):
            raise ValueError('Player name and style cannot be None')
        
        self.style = style
        self.name = name
    
    def get_player_style(self):    
        return self.style
    
    def get_player_name(self):
        return self.name
    
    
