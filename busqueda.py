import json
from estado import Estado
from casilla import Casilla
from nodo import Nodo
import heapq


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
           

        return initial,objetive 

    def creacion_sucesores(self,estado):
        f,c =estado.get_tupla()
        funcion_sucesores=[]
        sucesores=[]
        lista_vecinos=estado.get_vecinos()
        
        for i in lista_vecinos:
            if(i==(f-1,c)):
               sucesores=['N',(f-1,c),estado.get_valor()+1]
               funcion_sucesores.append(sucesores) 
            elif(i==(f,c+1)):
                sucesores=['E', (f,c+1),estado.get_valor()+1] 
                funcion_sucesores.append(sucesores) 
            elif(i==(f+1,c)):
                sucesores=['S', (f+1,c), estado.get_valor()+1] 
                funcion_sucesores.append(sucesores)
            elif(i==(f,c-1)):
                sucesores=['O', (f,c-1), estado.get_valor()+1]
                funcion_sucesores.append(sucesores)
        
        return funcion_sucesores
    
    def nodo_a_estado(self, nodo, estados):
        estado=0

        for i in estados:
            
            if(nodo.get_id_estado()==i.get_tupla()):
                estado=i
        return estado


    def generar_vecinos(self,estado):
        f,c=estado.get_tupla()
        lista_vecinos=[]
        if(estado.get_N()==True):
            vecinos= (f-1,c)
            lista_vecinos.append(vecinos)
        
        if(estado.get_E()==True):
            vecinos= (f,c+1) 
            lista_vecinos.append(vecinos) 
    
        if(estado.get_S()==True):
            vecinos= (f+1,c)
            lista_vecinos.append(vecinos)
    
        if(estado.get_O()==True):
            vecinos= (f,c-1)
            lista_vecinos.append(vecinos)

        return lista_vecinos

    def generar_estados(self, casillas):
        estados=[]
        
        for i in casillas:
            
            f,c=i.get_tupla()
            valor=i.get_valor()
            estado=Estado((f,c),valor)
            estado.set_N(i.get_N())
            estado.set_E(i.get_E())
            estado.set_S(i.get_S())
            estado.set_O(i.get_O())
            listas_vecinos=self.generar_vecinos(estado)
            
            estado.set_vecinos(listas_vecinos)
            estados.append(estado)
        return estados
    

    
    def reorden_frontera(self, frontera, lista_nodos,circuito):
        
        for i in lista_nodos:
            repetido=False
            for j in circuito:
                if j.get_id_estado()==i.get_id_estado():
                    repetido=True
            if repetido==False:
                f,c=i.get_id_estado()
                A=(i.get_valor(),f,c,i.get_id_estado(),i)
                heapq.heappush(frontera,A)





                '''nodo_aux=i
                tamanio_frontera=frontera.qsize()
               
                j=0
                while j<tamanio_frontera:
                    nodo_comparacion=frontera.get()
                   
                    if(nodo_comparacion.get_valor()==nodo_aux.get_valor()):
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
                
                frontera.put(nodo_aux)'''
                
           
        return frontera
    
    def creacion_nodo(self, funcion_sucesores, id, costo,estado,heuristica,profundidad , estrategia , objetivo):
        lista_nodos=[]
        valor=0
        for i in funcion_sucesores:
            if(id!=0):
                id_padre= estado.get_tupla()
                id_estado= i[1]
                accion=i[0]
                costo= estado.get_costo() +  i[2]
                valor=self.value(i,estrategia)
                heuristica=self.heuristic(nodo , id_estado , objetivo.get_tupla()) 
              
            else:
                id_padre= None
                id_estado=i.get_tupla()
                accion=None
                costo=0
                valor=valor(i,estrategia)  
                heuristica=heuristica(nodo , id_estado , objetivo.get_tupla()) 
                
            id+=1
            nodo=Nodo(id,costo,id_estado,id_padre,accion,profundidad,heuristica,valor)
            
            lista_nodos.append(nodo)
            nodo.set_profundidad(profundidad+1)
        
        return lista_nodos,id, costo, profundidad, heuristica, valor

        '''En este metodo he cambiado como calcular el valor y la heuristica , falta mirar bien como cambiar el costo ( hay que cambiar tanto el costo de cada nodo '''
        '''y luego el costo total), creo que deberiamos pasarle la lista estados y utilizar el metodo nodotoestado y coger de ahi el valor y sumarle 1 y el cost general''' 

    def conversion_estado(self, estado, estados):
        aux=0
        valor1=estado.split(',')[0].split('(')[1]
        valor2=estado.split(',')[1].split(')')[0]
        estado=(int(valor1),int(valor2))
        for i in estados:
            if(estado==i.get_tupla()):
                aux=i
                
        return aux
        
    def objetivo(self, estado_objetivo,estado):
        if(estado_objetivo==estado):
            return True
        
    
    def value(self , nodo , estrategia): 
        if estrategia=='BREADTH': 
            valor= nodo.get_profundidad()

        elif estrategia =='DEPTH':
            valor= 1/(nodo.get_profundidad()+1)

        elif estrategia == 'UNIFORM':
            valor= nodo.get_costo()

        elif estrategia == ' GREDDY':
            valor= nodo.get_heurisitica()

        elif estrategia == 'A' :
            valor= nodo.get_costo() + nodo.get_heurisitica()
        return valor

    '''Estos metodos hay que revisarle , pero juraria que esta bien'''
    


    def heurisitica(self, nodo , estado , objetivo): 
        f,c=estado
        f1,c1=objetivo
        DisManhattan= abs(f-f1)+ abs(c-c1)
        return DisManhattan