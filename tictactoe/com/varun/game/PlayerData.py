'''
Created on Apr 21, 2018

@author: varunjai
'''
class PlayerData(object):
    def __init__(self, name: str, style: str):
        self.name = name
        self.style = style
    
    def get_player_style(self):    
        return self.style
    
    def get_player_name(self):
        return self.name    