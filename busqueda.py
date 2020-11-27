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
           

        return initial,objetive,maze

    def creacion_sucesores(self,estado,lista_estados):
        f,c =estado.get_tupla()
        funcion_sucesores=[]
        sucesores=[]
        lista_vecinos=estado.get_vecinos()
        
        
        for i in lista_vecinos:
            if(i==(f-1,c)):
                sucesor=self.conversion_estado(str((f-1,c)),lista_estados)
                sucesores=['N',(f-1,c),sucesor.get_valor()+1]
                funcion_sucesores.append(sucesores) 
            elif(i==(f,c+1)):
                sucesor=self.conversion_estado(str((f,c+1)),lista_estados)
                sucesores=['E', (f,c+1),sucesor.get_valor()+1] 
                funcion_sucesores.append(sucesores) 
            elif(i==(f+1,c)):
                sucesor=self.conversion_estado(str((f+1,c)),lista_estados)
                sucesores=['S', (f+1,c), sucesor.get_valor()+1] 
                funcion_sucesores.append(sucesores)
            elif(i==(f,c-1)):
                sucesor=self.conversion_estado(str((f,c-1)),lista_estados)
                sucesores=['O', (f,c-1), sucesor.get_valor()+1]
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
                A=(i.get_valor(),f,c,i.get_id(),i)
                
                heapq.heappush(frontera,A)
                
           
        return frontera
    
    def creacion_nodo(self, funcion_sucesores, identificador, estado,estrategia,  objetivo,nodo_padre):
        lista_nodos=[]
        valor=0
        heuristica=0
        costo=0
        
        for i in funcion_sucesores:
            
            if(identificador!=0):
                id_padre= nodo_padre.get_id()
                id_estado= i[1]
                accion=i[0]
                profundidad=nodo_padre.get_profundidad()+1
                
                costo= nodo_padre.get_costo() +  i[2]  
                 
            else:
                id_padre= None
                id_estado=i.get_tupla()
                accion=None
                profundidad=0
                costo=0
            
            nodo=Nodo(identificador,costo,id_estado,id_padre,accion,profundidad,heuristica,valor)
            
            heuristica=self.heuristic(nodo , id_estado , objetivo.get_tupla())
            nodo.set_heuristica(heuristica)
            valor=self.value(nodo,estrategia)
            

            identificador+=1
            
            nodo.set_valor(valor) 
            print(nodo.get_id(),nodo.get_id_estado(), nodo.get_id_padre(),nodo.get_valor()) 
           
            lista_nodos.append(nodo)
            
        
        return lista_nodos,identificador

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
            valor= (1/(nodo.get_profundidad()+1))

        elif estrategia == 'UNIFORM':
            valor= nodo.get_costo()

        elif estrategia == 'GREEDY':
            valor= nodo.get_heuristica()

        elif estrategia == 'A' :
            valor= nodo.get_costo() + nodo.get_heuristica()
            

        return valor

    '''Estos metodos hay que revisarle , pero juraria que esta bien'''
    


    def heuristic(self, nodo , estado , objetivo): 
        f,c=estado
        f1,c1=objetivo
        DisManhattan= abs(f-f1)+ abs(c-c1)
        return DisManhattan

    def imprimir_solucion(self, lista_solucion,fila,columna,estrategia):
        fichero='sol_{}x{}_{}.txt'.format(fila,columna,estrategia)
        with open(fichero,'w') as f:
            f.write('[id][cost,state,father_id,action,depth,h,value]\n')
            for i in lista_solucion:
                f.write('[{}][{},{},{},{},{},{},{}]\n'.format(i.get_id(),i.get_costo(),i.get_id_estado(),i.get_id_padre(),i.get_accion(),i.get_profundidad(),i.get_heuristica(),i.get_valor()))

    def encontrar_solucion(self, circuitofinal, estado_inicial):
        lista_solucion=[]
        circuitofinal= list(reversed(circuitofinal))
        
        nodo_final=circuitofinal[0]
        lista_solucion.append(nodo_final)
        nodo_aux=nodo_final
        while (nodo_aux.get_id_estado()!=estado_inicial.get_tupla()):
            for i in circuitofinal:
                f0,c0=nodo_aux.get_id_estado()
                f1,c1=i.get_id_estado()
                if(nodo_aux.get_accion()=='N'):
                    if(f1==f0+1 and c1==c0):
                        nodo_aux=i
                        lista_solucion.append(nodo_aux)

                if(nodo_aux.get_accion()=='S'):
                    if(f1==f0-1 and c1==c0):
                        nodo_aux=i
                        lista_solucion.append(nodo_aux)

                if(nodo_aux.get_accion()=='E'):
                    if(f1==f0 and c1==c0-1):
                        nodo_aux=i
                        lista_solucion.append(nodo_aux)
                
                if(nodo_aux.get_accion()=='O'):
                    if(f1==f0 and c1==c0+1):
                        nodo_aux=i
                        lista_solucion.append(nodo_aux)

        return list(reversed(lista_solucion))


            




            
