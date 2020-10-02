import json
from random import randint
class Laberinto(object):
    def __init__(self,fichero_json=None,*args,**kwargs):

        with open(fichero_json) as f:
            datos=f.read()
        datos=json.loads(datos)
        self.filas=datos["rows"]
        self.columnas=datos["cols"]
        self.max_nmax_n=datos["max_n"]
        self.mov=datos["mov"]
        self.id_mov=datos["id_mov"]
        self.cells=datos["cells"]
        self.value=[]
        self.celdas=[]
        for entity in self.cells:
            entityName = entity #(0, 0)  (0, 1) 
            v=self.cells[entityName]["value"]
            neighbors=self.cells[entityName]["neighbors"]
            self.value.append(v)
            self.celdas.append(neighbors)

    def movimiento_valido(self,casilla_actual,no_visitados,visitados):
        f,c=casilla_actual
        
        if f-1:
            return True
        else if:
        else if:
        else if:
            return True 
        
    def tablero(self):
        camino=[]
        visitados=[]
        no_visitados=[]
        casilla_destino=(randint(0,self.filas),randint(0,self.columnas))
        visitados.append(casilla_destino)
        casilla_inicio=(randint(0,self.filas),randint(0,self.columnas))
        while(casilla_inicio in visitados):
            casilla_inicio=(randint(0,self.filas),randint(0,self.columnas))
        
        camino = [0] * self.filas
        for i in range(self.filas):
            camino[i] = [0] * self.columnas
        self.movimiento_valido(casilla_inicio,no_visitados,visitados)


a=Laberinto("fichero.json")
a.tablero()