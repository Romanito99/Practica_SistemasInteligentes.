import json
from random import randint
from casilla import Casilla

class Laberinto(object):
    def __init__(self,fichero_json=None,*args,**kwargs):
        if (len(args)!=1):
            try:
                with open(fichero_json) as f:
                    datos=f.read()
                datos=json.loads(datos)
            except:
                print("No se ha podido leer el fichero json")
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
            else:
                self.filas=
                self.columnas=
        else:
            self.filas=args[0]
            self.columnas=args[1]
            self.tablero,self.casillas=self.generar_tuplas(self.filas,self.columnas)
            

    def movimiento_valido(self,no_visitados,visitados,casilla_destino,camino, casillas):
    while(len(no_visitados)!=0):
        casilla_actual=(randint(0,self.filas-1),randint(0,self.columnas-1))
        while(casilla_actual in visitados):
            casilla_actual=(randint(0,self.filas-1),randint(0,self.columnas-1))
        camino.append(casilla_actual)
        no_visitados.remove(casilla_actual)
       
    
        while(casilla_actual not in visitados):
            
            f,c=casilla_actual
            movimiento=self.movimiento_random(f,c)
            if(movimiento==0):
                if  ((f-1,c) in no_visitados): #Norte 
                    
                    casilla_actual=(f-1,c)
                    camino.append(casilla_actual)
                    no_visitados.remove(casilla_actual)
                
                else: 
                    if(f-1,c) in camino:
                        n=camino.index((f-1,c))
                        camino=camino[:n+1]
                        casilla_actual=(f-1,c)
                    elif (f-1,c) in visitado:
                        casilla_actual=(f-1,c)
                        visitados.remove(casilla_actual)
                        camino.append(casilla_actual)
                        self.excavar(camino,visitados,casillas)

            elif(movimiento==1):
            
                if ((f,c+1) in no_visitados): #Este 
                    casilla_actual=(f,c+1)
                    camino.append(casilla_actual)
                    no_visitados.remove(casilla_actual)

                else: 
                    if(f,c+1) in camino:
                        n=camino.index((f,c+1))
                        camino=camino[:n+1]
                        casilla_actual=(f,c+1)
                    elif (f,c+1) in visitado:
                        casilla_actual=(f,c+1)
                        visitados.remove(casilla_actual)
                        camino.append(casilla_actual)
                        self.excavar(camino,visitados,casillas)
            
            elif (movimiento==2):
                 if  ((f+1,c) in no_visitados): #sur
                    casilla_actual=(f+1,c)
                    camino.append(casilla_actual)
                    no_visitados.remove(casilla_actual)
                
                else: 
                    if(f+1,c) in camino:
                        n=camino.index((f+1,c))
                        camino=camino[:n+1]
                        casilla_actual=(f+1,c)
                    elif (f+1,c) in visitado:
                        casilla_actual=(f+1,c)
                        visitados.remove(casilla_actual)
                        camino.append(casilla_actual)
                        self.excavar(camino,visitados,casillas)
            
            elif(movimiento==3):
                 if ((f,c-1) in no_visitados): #Este 
                    casilla_actual=(f,c-1)
                    camino.append(casilla_actual)
                    no_visitados.remove(casilla_actual)

                else: 
                    if(f,c-1) in camino:
                        n=camino.index((f,c-1))
                        camino=camino[:n+1]
                        casilla_actual=(f,c-1)
                    elif (f,c-1) in visitado:
                        
                        casilla_actual=(f,c-1)
                        visitados.remove(casilla_actual)
                        camino.append(casilla_actual)
                        self.excavar(camino,visitados,casillas)
                
    def excavar(self,camino,visitados,casillas):
        n=0
        while(n<(len(camino)-1)):
            f0,c0=camino[n]
            f1,c1=camino[n+1]
            encontrado=False
            i=0
            while(encontrado==False):
                if(casillas[i].get_tupla()==camino[n]): 
                    encontrado==True
                i+=1

            f2=f1-f0
            c2=c1-c0

            if(f2==-1): 
                casillas[i].set_N(True)
                casillas[i-self.columnas].set_S(True)    
            elif(f2==1):
                casillas[i].set_S(True)
                casillas[i+self.columnas].set_N(True)
            elif(c2==-1):
                casillas[i].set_O(True)
                casillas[i-1].set_E(True)
            elif(c2==1):
                casillas[i].set_E(True)
                casillas[i+1].set_O(True)
            n+=1
            
        visitados.extend(camino)
        camino=[]

    def generar_tuplas(self):
        tuplas=[]
        casillas=[]
        i=0
        j=0
        while i<self.columnas:
            t=(i,0)
            while j<self.filas:
                t=(i,j)
                casilla=Casilla(t,0)
                tuplas.append(t)
                casillas.append(casilla)
                j+=1

            i+=1
            j=0
        return tuplas,casillas


        
    def tablero(self):
        camino=[]
        visitados=[]
        no_visitados=self.generar_tuplas()
        casilla_destino=(randint(0,self.filas-1),randint(0,self.columnas-1))
        visitados.append(casilla_destino)
        no_visitados.remove(casilla_destino)
        camino = [0] * self.filas
        for i in range(self.filas):
            camino[i] = [0] * self.columnas
        self.movimiento_valido(no_visitados,visitados,casilla_destino,camino,casilla_inicio, casillas)

    def movimiento_random(self,filas,columnas):
        lista_movimientos=[0,1,2,3]
        if (filas==0):
            lista_movimientos.remove(0) #norte 
        elif (filas==self.filas-1):
            lista_movimientos.remove(2) #sur
        
        if (columnas==0):
            lista_movimientos.remove(1) #Este
        elif (columnas==self.columnas-1):   
            lista_movimientos.remove(3) #Oeste 
        
        numero=randint(0,len(lista_movimientos))
        numero=lista_movimientos.index(numero)
        return numero

a=Laberinto("fichero.json")
a.tablero()
