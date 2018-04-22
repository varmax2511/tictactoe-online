'''
Created on Apr 19, 2018
Each piece will have style associated with it, like
X or O
@author: varunjai
'''


class Piece(object):

    def __init__(self, style: str):
        self.style = style
    
    def get_style(self):     
        return self.style