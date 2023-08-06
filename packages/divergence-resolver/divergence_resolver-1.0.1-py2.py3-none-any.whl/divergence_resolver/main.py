# -*- coding: UTF-8 -*-
 
from random import choice

class Divergence:

    def __init__(self,name='robot'):
        self.name = name
        pass

    def getChoice(self,name=None):
        if name is not None:
            self.name = name
        self.__lists = ['剪刀','石头','布']
        result = choice(self.__lists)
        print(self.name,':选择了>',result)

def YourChoice(name='robot'):
    p = Divergence()
    p.getChoice(name)