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
    def movimiento_valido(self,no_visitados,visitados,casilla_destino,camino,casilla_actual):
        camino.append(casilla_actual)
        no_visitados.remove(casilla_actual)
        f,c=casilla_actual
        print(casilla_actual)
        vecinos=self.celdas[f*self.columnas+c]
        if vecinos[0]==True and ((f-1,c) in no_visitados): #Norte 

            return True
        elif vecinos[1]==True and ((f,c+1) in no_visitados): #Este 
            return True
        elif vecinos[2]==True and ((f+1,c) in no_visitados): #Sur
            return True
        elif vecino[3]==True and ((f,c-1) in no_visitados):  #Oeste 
            return True



    def generar_tuplas(self):
        tuplas=[]
        i=0
        j=0
        while i<self.columnas:
            t=(i,0)
            while j<self.filas:
                t=(i,j)
                tuplas.append(t)
                j+=1

            i+=1
            j=0
        return tuplas


        
    def tablero(self):
        camino=[]
        visitados=[]
        no_visitados=self.generar_tuplas()
        casilla_destino=(randint(0,self.filas-1),randint(0,self.columnas-1))
        visitados.append(casilla_destino)
        no_visitados.remove(casilla_destino)
        casilla_inicio=(randint(0,self.filas-1),randint(0,self.columnas-1))
        while(casilla_inico in visitados):
            casilla_inicio=(randint(0,self.filas-1),randint(0,self.columnas-1))

        
        
        camino = [0] * self.filas
        for i in range(self.filas):
            camino[i] = [0] * self.columnas
        self.movimiento_valido(no_visitados,visitados,casilla_destino,camino,casilla_inicio)


a=Laberinto("fichero.json")
a.tablero()
