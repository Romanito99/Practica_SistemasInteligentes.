import json
from estado import Estado
from casilla import Casilla
from nodo import Nodo
import queue

class Busqueda():
    def tojson(self,laberinto_json,inicial,objetivo):
        data={}
        tupla_inicial="{}".format(inicial)
        tupla_objetivo="{}".format(objetivo)
        data['INITIAL']=tupla_inicial
        data['OBJETIVE']=tupla_objetivo
        data['MAZE']=laberinto_json

        with open('problema.json','w') as f:
            json.dump(data, f, indent=4)

    def readjson(self,fichero_json):
        try:
            with open(fichero_json) as f:
                datos=f.read()
            datos=json.loads(datos)
        except:
            print("No se ha podido leer el fichero json de busqueda")
        else:
            initial=datos['INITIAL']
            objetive=datos['OBJETIVE']
            maze=datos['MAZE']
        
    def creacion_sucesores(self,estado, lista_movimiento):
        f,c =estado.get_tupla()
        funcion_sucesores=[]
        sucesores=[]
        if 0 in lista_movimiento:
            if(estado.get_N()==False):
                sucesores=['N', (f-1,c), 1] 
                funcion_sucesores.append(sucesores)
        if 1 in lista_movimiento:
            if(estado.get_E()==False):
                sucesores=['E', (f,c+1), 1] 
                funcion_sucesores.append(sucesores) 
        if 2 in lista_movimiento:
            if(estado.get_S()==False):
                sucesores=['S', (f+1,c), 1] 
                funcion_sucesores.append(sucesores)
        if 3 in lista_movimiento:
            if(estado.get_O()==False):
                sucesores=['O', (f,c-1), 1]
                funcion_sucesores.append(sucesores)
        return funcion_sucesores

        

    def generar_estados(self, casillas):
        estados=[]
        for i in casillas:
            f,c=i.get_tupla()
            valor=i.get_valor()
            estado=Estado((f,c),valor)
            estados.append(estado)
        return estados
    

    def movimiento_permitido(self,filas,columnas, estado):
        '''Movimiento aleatorio para decidir si vamos al N,E,S o O'''
        lista_movimientos=[0,1,2,3]
        f,c=estado.get_tupla()

        if (f==0):
            lista_movimientos.remove(0) #norte
        elif (f==filas-1):
            lista_movimientos.remove(2) #sur
        if (c==0):
            lista_movimientos.remove(3) #Este
        elif (c==columnas-1):
            lista_movimientos.remove(1) #Oeste
        
        return lista_movimientos
    
    def reorden_frontera(self, frontera, lista_nodos):
        for i in lista_nodos:
            nodo_aux=i.get_id_estado()
            tamanio_frontera=frontera.qsize()
            j=0
            while j<tamanio_frontera:
                nodo_comparacion=frontera.get()
                if(nodo_comparacion==nodo_aux.get_valor()):
                    f0,c0=nodo_comparacion.get_id_estado()
                    f1,c1=nodo_aux.get_id_estado()
                    if(f0==f1):
                        if(c0>c1):
                            frontera.put(nodo_aux)
                            nodo_aux=nodo_comparacion
                        else:
                            frontera.put(nodo_comparacion)

                    elif(f0>f1):
                        frontera.put(nodo_aux)
                        nodo_aux=nodo_comparacion
                    else:
                        frontera.put(nodo_comparacion)

                elif(nodo_comparacion.get_valor()>nodo_aux.get_valor()):
                    frontera.put(nodo_aux)
                    nodo_aux=nodo_comparacion
                else:
                    frontera.put(nodo_comparacion)
                j+=1
            frontera.put(nodo_aux)

        return frontera
    
    def creacion_nodo(self, funcion_sucesores, id):
        lista_nodos=[]
        for i in funcion_sucesores:
            
            id+=1
        return lista_nodos,id

    def problema(self, objetivo, estado):
        frontera= queue.PriorityQueue()
        funcion_sucesores=[]
        funcion_sucesores.append(estado)
        lista_nodos,id=self.creacion_nodo(funcion_sucesores,0)
        frontera.put(lista_nodos)
        while(objetivo()!=True):
            lista_movimiento=self.movimiento_permitido(4,4,estado)
            funcion_sucesores=self.creacion_sucesores(estado, lista_movimiento)
            lista_nodos, id=self.creacion_nodo(funcion_sucesores, id)
            frontera=self.reorden_frontera(frontera, lista_nodos)


    


