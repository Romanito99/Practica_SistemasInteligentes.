import json
from time import sleep
from random import randint
from casilla import Casilla
import matplotlib.pyplot as plt

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
            self.filas=10
            self.columnas=10
            #self.tablero,self.casillas=self.generar_tuplas(self.filas,self.columnas)
            

    def movimiento_valido(self,no_visitados,visitados,casilla_destino,camino, casillas): 
        while(len(no_visitados)!=0):
            x=[]
           
            casilla_actual=(randint(0,self.columnas-1),randint(0,self.filas-1))
            while(casilla_actual in visitados):
                casilla_actual=(randint(0,self.columnas-1),randint(0,self.filas-1))
            camino.append(casilla_actual)
            no_visitados.remove(casilla_actual)
        
            
            while(casilla_actual not in visitados):
                
                f,c=casilla_actual
                movimiento=self.movimiento_random(f,c)
                if(movimiento==0):
                    
                    #sleep(2)
                    if  ((f-1,c) in no_visitados): #Norte 
                        
                        casilla_actual=(f-1,c)
                        camino.append(casilla_actual)
                        no_visitados.remove(casilla_actual)
                        
                        

                    else: 
                        if(f-1,c) in camino:
                            #print("entro a camino")
                            n=camino.index((f-1,c))
                            x=camino[n+1:]
                            no_visitados.extend(x)
                            camino=camino[:n+1]
                            

                            casilla_actual=(f-1,c)
                        elif (f-1,c) in visitados:
                            #print("entro a visitado")
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
                            #print("entro a camino")
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
                    
                    #sleep(2)
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
                casillas[i-self.filas].set_S(True)
                
               
                
                
                #sleep(10)
                   
            if(f2==1):
                casillas[i].set_S(True)
                casillas[i+self.filas].set_N(True)
                
                #sleep(10)
            if(c2==-1):
                casillas[i].set_O(True)
                casillas[i-1].set_E(True)
                visitado=i-1
                
                #sleep(10)

            if(c2==1):
                casillas[i].set_E(True)
                casillas[i+1].set_O(True)
                
                #sleep(10)
            n+=1
            
        visitados.extend(camino)
        camino=[]
        return camino,casillas,visitados

    def generar_tuplas(self):
        tuplas=[]
        casillas=[]
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
        camino=[]
        visitados=[]
        casillas=[]
        no_visitados,casillas=self.generar_tuplas()
        casilla_destino=(randint(0,self.columnas-1),randint(0,self.filas-1))
        print(casilla_destino)
        print(no_visitados)
        visitados.append(casilla_destino)
        print(visitados)
        no_visitados.remove(casilla_destino)
        
       
       
        casillas=self.movimiento_valido(no_visitados,visitados,casilla_destino,camino, casillas)
        return casillas


    def movimiento_random(self,filas,columnas):
        
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
        plt.figure(figsize=(self.columnas+0.1, self.filas+0.1))
        
        plt.axvspan(-0.1, self.columnas+0.1, facecolor='black', alpha=2)
        plt.axvspan(-0.1, self.filas+0.1, facecolor='black', alpha=2)
        plt.ylim(self.columnas+0.1,-0.1)
        plt.xlim(-0.1,self.filas+0.1)
        plt.style.use('dark_background')
        for i in casillas:
            
            c,f=i.get_tupla()
            #sleep(5)
            if (i.get_S()==False):
                
                plt.plot([f,f+1],[c+1,c+1],color='white',linewidth=3.0)
            else:
                plt.plot([f,f+1],[c+1,c+1],color='dimgray',linestyle="--")
            if (i.get_E()==False):
            
                plt.plot([f+1,f+1],[c,c+1],color='white',linewidth=3.0)
            else:   
                plt.plot([f+1,f+1],[c,c+1],color='dimgray',linestyle="--")
            if (i.get_N()==False):
                
                plt.plot([f,f+1],[c,c],color='white',linewidth=3.0)
            else:
                plt.plot([f,f+1],[c,c],color='dimgray',linestyle="--")
            if (i.get_O()==False):
                
                plt.plot([f,f],[c,c+1],color='white',linewidth=3.0)
            else:
                plt.plot([f,f],[c,c+1],color='dimgray',linestyle="--")
        
        plt.savefig("laberinto.png")

    def to_json(self,casillas):
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


        with open("jesus.json", "w") as f:
            json.dump(data, f,indent=4)

a=Laberinto(4,4)
lista=a.tablero()
a.to_json(lista)
a.dibujar(lista)
