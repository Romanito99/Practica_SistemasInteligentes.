from casilla import Casilla 
class Estado(Casilla):
    def __init__(self,tupla,valor,vecinos=[]):
        Casilla.__init__(self,tupla,valor)
        self.vecinos=vecinos

    
    def set_vecinos(self,v):
        self.vecinos=v
    
    def get_vecinos(self):
        return self.vecinos
