class Laberinto(object):
    def __init__(self,filas,columnas,value,celdas=[]):
        self.filas=filas
        self.columnas=columnas
        self.celdas=celdas
        self.value=value

    
    def get_filas(self):
        return self.filas

    def get_columnas(self):
        return self.columnas

    def get_celdas(self):
        return self.celdas

    def set_filas(self,f):
        self.filas=f

    def set_columnas(self,c):
        self.columnas=c

    def set_celdas(self,v):
        self.celdas.append(v)