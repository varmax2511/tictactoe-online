'''
Created on Apr 20, 2018

@author: varunjai
'''
from com.varun.player.Player import Player

class HumanPlayer(Player):
    
    def __init__(self, name: str, style: str):
        Player.__init__(self, name, style)
    
        
