import json
from random import randint
from casilla import Casilla
import matplotlib.pyplot as plt
from busqueda import Busqueda
from nodo import Nodo
import queue
from time import sleep
import heapq

class Laberinto(object):
    def __init__(self,*args,**kwargs):
        '''Metodo constructor de la clase laberinto'''
        
        self.prueba=2
        if (len(args)==1):
            self.read_json(args[0])
            if(not self.comprobar_integridad()):
                self.dibujar(self.casillas)
            else:
                print("Ha dado error en el json")

        else:
            self.filas=args[0]
            self.columnas=args[1]
            self.casillas=self.tablero()
            self.to_json(self.casillas)
            self.dibujar(self.casillas)

        #estado,frontera,circuitofinal=self.problema()
        #print("HAS LLEGADO AL OBJETIVO",estado.get_tupla())


    def movimiento_valido(self,no_visitados,visitados,casilla_destino,camino, casillas):
        '''En este metodo se realiza el algoritmo de Wilson'''

        while(len(no_visitados)!=0):
            x=[]

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
                            x=camino[n+1:]
                            no_visitados.extend(x)
                            camino=camino[:n+1]
                            casilla_actual=(f-1,c)
                        elif (f-1,c) in visitados:
                            casilla_actual=(f-1,c)
                            visitados.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,visitados=self.excavar(camino,visitados,casillas)

                elif(movimiento==1):

                    if ((f,c+1) in no_visitados): #Este
                        casilla_actual=(f,c+1)
                        camino.append(casilla_actual)
                        no_visitados.remove(casilla_actual)
                    else:
                        if(f,c+1) in camino:
                            n=camino.index((f,c+1))
                            x=camino[n+1:]
                            no_visitados.extend(x)
                            camino=camino[:n+1]

                            casilla_actual=(f,c+1)
                        elif (f,c+1) in visitados:

                            casilla_actual=(f,c+1)
                            visitados.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,visitados= self.excavar(camino,visitados,casillas)

                elif (movimiento==2):
                    if  ((f+1,c) in no_visitados): #sur
                        casilla_actual=(f+1,c)
                        camino.append(casilla_actual)
                        no_visitados.remove(casilla_actual)
                    else:
                        if(f+1,c) in camino:

                            n=camino.index((f+1,c))
                            x=camino[n+1:]
                            no_visitados.extend(x)
                            camino=camino[:n+1]
                            casilla_actual=(f+1,c)
                        elif (f+1,c) in visitados:

                            casilla_actual=(f+1,c)
                            visitados.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,visitados=self.excavar(camino,visitados,casillas)

                elif(movimiento==3):
                    if ((f,c-1) in no_visitados): #Este
                        casilla_actual=(f,c-1)
                        camino.append(casilla_actual)
                        no_visitados.remove(casilla_actual)

                    else:
                        if(f,c-1) in camino:
                            n=camino.index((f,c-1))
                            x=camino[n+1:]
                            no_visitados.extend(x)
                            camino=camino[:n+1]
                            casilla_actual=(f,c-1)

                        elif (f,c-1) in visitados:
                            casilla_actual=(f,c-1)
                            visitados.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,visitados=self.excavar(camino,visitados,casillas)
        return casillas

    def excavar(self,camino,visitados,casillas):
        '''Metodo que nos "excava" el camino escogido'''
        n=0
        while(n<(len(camino)-1)):
            f0,c0=camino[n]
            f1,c1=camino[n+1]

            encontrado=False
            i=0
            while(encontrado==False):

                if(casillas[i].get_tupla()==camino[n]):
                    encontrado=True
                else:
                    i+=1
            f2=f1-f0
            c2=c1-c0

            if(f2==-1):
                casillas[i].set_N(True)
                casillas[i-self.columnas].set_S(True)
            if(f2==1):
                casillas[i].set_S(True)
                casillas[i+self.columnas].set_N(True)
            if(c2==-1):
                casillas[i].set_O(True)
                casillas[i-1].set_E(True)
            if(c2==1):
                casillas[i].set_E(True)
                casillas[i+1].set_O(True)

            n+=1

        visitados.extend(camino)
        camino=[]
        return camino,casillas,visitados

    def generar_tuplas(self):
        ''' Generamos las tuplas (coordenadas) y sus respectivos objetos casilla'''
        tuplas=[]
        casillas=[]
        self.prueba=3
        i=0
        j=0
        while i<self.filas:
            t=(i,0)
            while j<self.columnas:
                t=(i,j)
                casilla=Casilla(t,0)
                tuplas.append(t)
                casillas.append(casilla)
                j+=1

            i+=1
            j=0
        return tuplas,casillas



    def tablero(self):
        '''Metodo principal que usamos para llamar al resto'''
        camino=[]
        visitados=[]
        casillas=[]
        no_visitados,casillas=self.generar_tuplas()
        casilla_destino=(randint(0,self.filas-1),randint(0,self.columnas-1))
        visitados.append(casilla_destino)
        no_visitados.remove(casilla_destino)



        casillas=self.movimiento_valido(no_visitados,visitados,casilla_destino,camino, casillas)
        return casillas


    def movimiento_random(self,filas,columnas):
        '''Movimiento aleatorio para decidir si vamos al N,E,S o O'''
        lista_movimientos=[0,1,2,3]

        if (filas==0):
            lista_movimientos.remove(0) #norte
        elif (filas==self.filas-1):
            lista_movimientos.remove(2) #sur

        if (columnas==0):
            lista_movimientos.remove(3) #Este
        elif (columnas==self.columnas-1):
            lista_movimientos.remove(1) #Oeste

        numero=randint(0,len(lista_movimientos)-1)



        numero=lista_movimientos[numero]


        return numero

    def dibujar(self,casillas):   
        
        '''Este metodo se usa para dibujar el laberinto e imprimir la imagen en .png'''
        plt.figure(figsize=(self.filas+0.1, self.columnas+0.1))

        plt.axhspan(-0.1, self.columnas+0.1, facecolor='black', alpha=2)
        
        
        plt.ylim(self.filas+0.1,-0.1)
        plt.xlim(-0.1,self.columnas+0.1)
        plt.style.use('dark_background')
        for i in casillas:
            

            f,c=i.get_tupla()
            
            if (i.get_S()==False):
                
                plt.plot([c,c+1],[f+1,f+1],color='white',linewidth=3.0)
            else:
                plt.plot([c,c+1],[f+1,f+1],color='dimgray',linestyle="--")
            if (i.get_E()==False):

                plt.plot([c+1,c+1],[f,f+1],color='white',linewidth=3.0)
            else:
                plt.plot([c+1,c+1],[f,f+1],color='dimgray',linestyle="--")
            if (i.get_N()==False):

                plt.plot([c,c+1],[f,f],color='white',linewidth=3.0)
            else:
                plt.plot([c,c+1],[f,f],color='dimgray',linestyle="--")
            if (i.get_O()==False):

                plt.plot([c,c],[f,f+1],color='white',linewidth=3.0)
            else:
                plt.plot([c,c],[f,f+1],color='dimgray',linestyle="--")
            
            '''if(i in hola):
                ymin=1-(f/self.filas) 
                print("hola",ymin)
                ymax=ymin - (1/self.filas)
                plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='yellow')'''
                
                
                

        plt.savefig("laberinto.png")

    def to_json(self,casillas):
        '''Se construye el json con la lista de casillas y sus atributos'''

        data={}
        tupla=""
        neighbours=''
        data['rows']=self.filas
        data['cols']=self.columnas
        data['max_n']=4
        data['mov']=[[-1,0],[0,1],[1,0],[0,-1]]
        data['id_mov']=["N","E","S","O"]
        data['cells']={}

        for i in casillas:
            t=i.get_tupla()
            value=i.get_valor()
            dicc_cells={}
            dicc_tuplas={}
            tupla="{}".format(t)
            neighbours=i.string()
            dicc_cells[tupla]= {}
            dicc_tuplas['value']=value
            dicc_tuplas['neighbors']=neighbours
            dicc_cells[tupla].update(dicc_tuplas)
            data['cells'].update(dicc_cells)


        with open("laberinto.json", "w") as f:
            json.dump(data, f,indent=4)

    def read_json(self,fichero_json):
        try:
            with open(fichero_json) as f:
                datos=f.read()
            datos=json.loads(datos)
        except:
            print("No se ha podido leer el fichero json")
        else:
            self.filas=datos["rows"]
            self.columnas=datos["cols"]
            self.max_nmax_n=datos["max_n"]
            self.mov=datos["mov"]
            self.id_mov=datos["id_mov"]
            self.cells=datos["cells"]
            self.casillas=[]
            for entity in self.cells:
                valor1=entity.split(',')[0].split('(')[1]
                valor2=entity.split(',')[1].split(')')[0]
                tupla=(int(valor1),int(valor2))
                v=self.cells[entity]["value"]
                neighbors=self.cells[entity]["neighbors"]
                #En un futuro debemos splitear y convertir en int a value
                casilla=Casilla(tupla,v)

                casilla.set_N(neighbors[0])
                casilla.set_E(neighbors[1])
                casilla.set_S(neighbors[2])
                casilla.set_O(neighbors[3])
                casilla.set_valor(v) 
                self.casillas.append(casilla)

    def comprobar_integridad(self):
        ''' En este metodo se comprueba la integridad del fichero json'''

        for i in self.casillas:
            f,c = i.get_tupla()
            if f==0:
                if i.get_N()==True:
                    return True
                j=self.casillas.index(i)+self.columnas
                if i.get_S()!=self.casillas[j].get_N():
                    return True
            elif f==self.filas-1:
                if i.get_S()==True:
                    return True
                j=self.casillas.index(i)-self.columnas
                if i.get_N()!=self.casillas[j].get_S():
                    return True
            else:
                j=self.casillas.index(i)+self.columnas
                if i.get_S()!=self.casillas[j].get_N():
                    return True
                j=self.casillas.index(i)-self.columnas
                if i.get_N()!=self.casillas[j].get_S():
                    return True
            if c==0:
                if i.get_O()==True:
                    return True
                j=self.casillas.index(i)+1
                if i.get_E()!=self.casillas[j].get_O():
                    return True
            elif c==self.columnas-1:
                if i.get_E()==True:
                    return True
                j=self.casillas.index(i)-1
                if i.get_O()!=self.casillas[j].get_E():
                    return True
            else:
                j=self.casillas.index(i)+1
                if i.get_E()!=self.casillas[j].get_O():
                    return True
                j=self.casillas.index(i)-1
                if i.get_O()!=self.casillas[j].get_E():
                    return True
        return False

    def problema(self):
        circuitofinal=[]
        b=Busqueda()
        frontera= []
        funcion_sucesores=[]
        estados=b.generar_estados(self.casillas)
        estado_inicial,estado_objetivo=b.readjson("prueba.json")
        
        estado_inicial=b.conversion_estado(estado_inicial,estados)
        estado_objetivo=b.conversion_estado(estado_objetivo,estados)
        
        funcion_sucesores.append(estado_inicial)
        
        lista_nodos, id, costo, profundidad, heuristica, valor = b.creacion_nodo(funcion_sucesores, 0, 0, None ,0,0)
        
        estado=estado_inicial
        frontera=b.reorden_frontera(frontera, lista_nodos,circuitofinal)
        while(b.objetivo(estado_objetivo,estado)!=True):  
            nodo=heapq.heappop(frontera)[3]
            circuitofinal.append(nodo)
            estado=b.nodo_a_estado(nodo,estados)
            funcion_sucesores=b.creacion_sucesores(estado)
            lista_nodos, id, costo, profundidad, heuristica, valor=b.creacion_nodo(funcion_sucesores, id, costo, estado,heuristica,profundidad)
            frontera=b.reorden_frontera(frontera, lista_nodos,circuitofinal)
            
        return estado ,frontera , circuitofinal 



a=Laberinto(4,4)