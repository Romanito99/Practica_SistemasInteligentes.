

class Casilla(object):
    def __init__(self, tupla,valor):
        self.tupla=tupla
        self.N=False
        self.E=False
        self.S=False
        self.O=False
        self.valor=valor 
    
    def get_tupla(self):
        return self.tupla
    def get_N(self):
        return self.N
    def get_E(self):
        return self.E
    def get_S(self):
        return self.S
    def get_O(self):
        return self.O
    def get_valor(self):
        return self.valor

    def set_tupla(self,t):
        self.tupla=t
    def set_N(self, N):
        self.N=N
    def set_E(self,E):
        self.E=E
    def set_S(self, S):
        self.S=S
    def set_O(self,O):
        self.O=O
    def set_valor(self,valor):
        self.valor=valor
    def string(self):
        s=[]
        s.append(self.N)
        s.append(self.E)
        s.append(self.S)
        s.append(self.O)
        return s
