import json
from random import randint
from casilla import Casilla
import matplotlib.pyplot as plt
from busqueda import Busqueda
from nodo import Nodo
import heapq
import os.path as path
import argparse
import os 

class Laberinto(object):
    def __init__(self,*args,**kwargs):
        '''Metodo constructor de la clase laberinto'''
        b=Busqueda()
        self.prueba=2
        if (len(args)==2) and isinstance(args[0],str) and isinstance(args[1],str):
            self.read_json(args[0])
            if(self.comprobar_integridad()):
                print("Ha dado error en el json")
            estado_inicial,estado_objetivo,maze=b.readjson(args[1])
        else:
            self.filas=args[0]
            self.columnas=args[1]
            self.casillas=self.tablero()
            self.to_json(self.casillas)
            estado_inicial=str((0,0))
            estado_objetivo=str((self.filas-1,self.columnas-1))
            maze=None       
        lista_estados=b.generar_estados(self.casillas)
        
        if(self.comprobar_integridad_fichero_nodos(estado_inicial,estado_objetivo,maze)):
            print('Introduzca la estrategia del problema\n')
            print('Las estrategias disponibles son: A, BREADTH, DEPTH, UNIFORM, GREEDY\n')
            estrategia=str(input('>>'))
            estrategia=estrategia.upper()            
            while  (estrategia!='A' and estrategia!='BREADTH' and estrategia!='DEPTH' and estrategia!='UNIFORM' and estrategia!='GREEDY'):
                print('Error introduciendo estrategia\n')
                print('RECUERDE: las estrategias disponibles son: A, BREADTH, DEPTH, UNIFORM, GREEDY\n')
                estrategia=str(input('>>'))
                estrategia=estrategia.upper()                
            estado,frontera,visitados,lista_solucion=self.problema(estado_inicial,estado_objetivo,maze,lista_estados,estrategia)
            self.dibujar(self.casillas,frontera,visitados,lista_solucion,estrategia)
            b.imprimir_solucion(lista_solucion,self.filas,self.columnas,estrategia)
        else:
            print("Finalizando programa....")


    def movimiento_valido(self,no_no_recorridos,no_recorridos,casilla_destino,camino, casillas):
        '''En este metodo se realiza el algoritmo de Wilson'''
        while(len(no_no_recorridos)!=0):
            x=[]
            casilla_actual=(randint(0,self.filas-1),randint(0,self.columnas-1))
            while(casilla_actual in no_recorridos):
                casilla_actual=(randint(0,self.filas-1),randint(0,self.columnas-1))
            camino.append(casilla_actual)
            no_no_recorridos.remove(casilla_actual)
            while(casilla_actual not in no_recorridos):
                f,c=casilla_actual
                movimiento=self.movimiento_random(f,c)
                if(movimiento==0):
                    if  ((f-1,c) in no_no_recorridos): #Norte
                        casilla_actual=(f-1,c)
                        camino.append(casilla_actual)
                        no_no_recorridos.remove(casilla_actual)
                    else:
                        if(f-1,c) in camino:
                            n=camino.index((f-1,c))
                            x=camino[n+1:]
                            no_no_recorridos.extend(x)
                            camino=camino[:n+1]
                            casilla_actual=(f-1,c)
                        elif (f-1,c) in no_recorridos:
                            casilla_actual=(f-1,c)
                            no_recorridos.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,no_recorridos=self.excavar(camino,no_recorridos,casillas)
                elif(movimiento==1):
                    if ((f,c+1) in no_no_recorridos): #Este
                        casilla_actual=(f,c+1)
                        camino.append(casilla_actual)
                        no_no_recorridos.remove(casilla_actual)
                    else:
                        if(f,c+1) in camino:
                            n=camino.index((f,c+1))
                            x=camino[n+1:]
                            no_no_recorridos.extend(x)
                            camino=camino[:n+1]
                            casilla_actual=(f,c+1)
                        elif (f,c+1) in no_recorridos:
                            casilla_actual=(f,c+1)
                            no_recorridos.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,no_recorridos= self.excavar(camino,no_recorridos,casillas)
                elif (movimiento==2):
                    if  ((f+1,c) in no_no_recorridos): #sur
                        casilla_actual=(f+1,c)
                        camino.append(casilla_actual)
                        no_no_recorridos.remove(casilla_actual)
                    else:
                        if(f+1,c) in camino:
                            n=camino.index((f+1,c))
                            x=camino[n+1:]
                            no_no_recorridos.extend(x)
                            camino=camino[:n+1]
                            casilla_actual=(f+1,c)
                        elif (f+1,c) in no_recorridos:
                            casilla_actual=(f+1,c)
                            no_recorridos.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,no_recorridos=self.excavar(camino,no_recorridos,casillas)
                elif(movimiento==3):
                    if ((f,c-1) in no_no_recorridos): #Este
                        casilla_actual=(f,c-1)
                        camino.append(casilla_actual)
                        no_no_recorridos.remove(casilla_actual)
                    else:
                        if(f,c-1) in camino:
                            n=camino.index((f,c-1))
                            x=camino[n+1:]
                            no_no_recorridos.extend(x)
                            camino=camino[:n+1]
                            casilla_actual=(f,c-1)
                        elif (f,c-1) in no_recorridos:
                            casilla_actual=(f,c-1)
                            no_recorridos.remove(casilla_actual)
                            camino.append(casilla_actual)
                            camino,casillas,no_recorridos=self.excavar(camino,no_recorridos,casillas)
        return casillas

    def excavar(self,camino,no_recorridos,casillas):
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
        no_recorridos.extend(camino)
        camino=[]
        return camino,casillas,no_recorridos

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
        no_recorridos=[]
        casillas=[]
        no_no_recorridos,casillas=self.generar_tuplas()
        casilla_destino=(randint(0,self.filas-1),randint(0,self.columnas-1))
        no_recorridos.append(casilla_destino)
        no_no_recorridos.remove(casilla_destino)
        casillas=self.movimiento_valido(no_no_recorridos,no_recorridos,casilla_destino,camino, casillas)
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

    def dibujar(self,casillas,frontera,visitados,lista_solucion,estrategia):          
        '''Este metodo se usa para dibujar el laberinto e imprimir la imagen en .png'''
        plt.figure(figsize=(self.columnas -1 , self.filas-1))
        plt.axhspan(-0.1, self.columnas+0.1, facecolor='black', alpha=2)       
        plt.ylim(self.filas+0.1,-0.1)
        plt.xlim(-0.1,self.columnas+0.1)
        plt.style.use('dark_background')
        for i in casillas:
            f,c=i.get_tupla()
            if (i.get_S()==False):
                plt.plot([c,c+1],[f+1,f+1],color='black',linewidth=3.0)  
            if (i.get_E()==False):
                plt.plot([c+1,c+1],[f,f+1],color='black',linewidth=3.0)           
            if (i.get_N()==False):
                plt.plot([c,c+1],[f,f],color='black',linewidth=3.0)           
            if (i.get_O()==False):
                plt.plot([c,c],[f,f+1],color='black',linewidth=3.0)

            if i.get_valor()==0:
                ymin=1-(f/self.filas)
                ymax=ymin - (1/self.filas)
                plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='white')
            elif i.get_valor()==1:
                ymin=1-(f/self.filas)
                ymax=ymin - (1/self.filas)
                plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='bisque')   
            elif i.get_valor()==2:
                ymin=1-(f/self.filas)
                ymax=ymin - (1/self.filas)
                plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='lightgreen')   
            elif i.get_valor()==3:
                ymin=1-(f/self.filas)
                ymax=ymin - (1/self.filas)
                plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='lightskyblue') 
            
            
            for j in frontera:
                if(i.get_tupla() == j[4].get_id_estado()):
                    ymin=1-(f/self.filas)
                    ymax=ymin - (1/self.filas)
                    plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='blue')
            for w in visitados:
                if(i.get_tupla() == w.get_id_estado()):
                    ymin=1-(f/self.filas)
                    ymax=ymin - (1/self.filas)
                    plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='lime')

            for u in lista_solucion:
                if(i.get_tupla() == u.get_id_estado()):
                    ymin=1-(f/self.filas)
                    ymax=ymin - (1/self.filas)
                    plt.axvspan(ymin=ymin,ymax=ymax,xmin=c,xmax=c+1,facecolor='red')        
               
        plt.savefig("solution_{}x{}_{}_20.png".format(self.filas,self.columnas,estrategia))

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

        fichero='Problema_{}x{}_maze.json'.format(self.filas,self.columnas)
        with open(fichero, "w") as f:
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

    def comprobar_integridad_fichero_nodos(self,estado_inicial,estado_objetivo,maze): 
        '''En este medoto comprobamos que el estado inicial y el estado objetivo esten dentro de los intervalos posibles , y que el fichero laberinto sea correcto'''       
        f_inicial=int(estado_inicial.split(',')[0].split('(')[1])
        c_inicial=int(estado_inicial.split(',')[1].split(')')[0])

        f_objetivo=int(estado_objetivo.split(',')[0].split('(')[1])
        c_objetivo=int(estado_objetivo.split(',')[1].split(')')[0])
        if(f_inicial<0 or c_inicial<0 or f_inicial>self.filas-1 or c_inicial>self.columnas-1):
            print("Error en el json")
            return False
        if (f_objetivo<0 or c_objetivo<0 or f_objetivo>self.filas-1 or c_objetivo>self.columnas-1):
            print("Error en el json")
            return False
        if maze is None:
            return True
        else:
            if not path.exists(maze):
                print("no existe el json principal")
                return False
            if path.exists(maze):
                maze=maze.split('_')
                filas_columnas=maze[1].split('x')
                filas=int(filas_columnas[0])
                columnas=int(filas_columnas[1])
                if filas!=self.filas or columnas!=self.columnas:
                    print("el fichero json no es correcto")
                    return False
                else:
                    return True
        


    def problema(self,estado_inicial,estado_objetivo,maze,lista_estados,estrategia):
        '''En este metoodo realizamos la resolucion del problema'''
        visitados=[]
        b=Busqueda()
        frontera= []
        funcion_sucesores=[]        
        estado_inicial=b.conversion_estado(estado_inicial,lista_estados)
        estado_objetivo=b.conversion_estado(estado_objetivo,lista_estados)        
        funcion_sucesores.append(estado_inicial)        
        lista_nodos, identificador = b.creacion_nodo(funcion_sucesores, 0, None ,estrategia,estado_objetivo,None)       
        estado=estado_inicial
        frontera=b.reorden_frontera(frontera, lista_nodos,visitados)

        while(b.objetivo(estado_objetivo,estado)!=True):           
            nodo,frontera=self.comprobarfrontera(visitados,frontera)
            visitados.append(nodo)
            estado=b.nodo_a_estado(nodo,lista_estados)
            funcion_sucesores=b.creacion_sucesores(estado,lista_estados)
            lista_nodos, identificador=b.creacion_nodo(funcion_sucesores, identificador,  estado,estrategia,estado_objetivo,nodo)
            frontera=b.reorden_frontera(frontera, lista_nodos,visitados)        
        frontera=self.comprobarfrontera2(visitados,frontera)       
        frontera=self.ultimosvecinos(lista_nodos,frontera)       
        lista_solucion=b.encontrar_solucion(visitados,estado_inicial)             
        return estado ,frontera , visitados,lista_solucion

    '''Los siguientes tres metodos los usamos para realizar la poda '''
    def comprobarfrontera(self,visitados,frontera):
        nodo=heapq.heappop(frontera)[4]
        if(len(frontera)!=0):
            for i in visitados:                   
                if nodo.get_id_estado()== i.get_id_estado():
                    nodo,frontera=self.comprobarfrontera(visitados,frontera)                    
        return nodo , frontera

    def comprobarfrontera2(self,visitados,frontera):
        
        if(len(frontera)!=0):
            for i in visitados:

                for j in frontera:
                    if(i.get_id_estado()==j[4].get_id_estado()):
                        frontera.remove(j)
        return  frontera

    def ultimosvecinos(self,lista_nodos,frontera):
        
        if(len(frontera)!=0):
            for i in lista_nodos: 
                for u in frontera:
                    if (i.get_id_estado()==u[4].get_id_estado()):
                        frontera.remove(u)
        return frontera


def argumentos():
    parser = argparse.ArgumentParser(description='nombre del archivo, numero de filas,numero de columnas, archivo problema. Debe  introducir filas y columnas(-r,-c) o archivo problema y archivo(-f,-p)')
    parser.add_argument("-r","--rows",required=False, help='numero de filas',type=int)
    parser.add_argument("-c","--columns",required=False,help='numero de columnas',type=int)
    parser.add_argument("-f","--file",required=False,help='archivo json',type=str)
    parser.add_argument("-p","--problem",required=False,help='archivo problema',type=str)
    args=parser.parse_args()
    return args

def main():
    args= argumentos()
    archivo_maze=args.file
    filas=args.rows
    columnas=args.columns
    archivo_problem=args.problem
    
    if archivo_maze is not None and archivo_problem is not None:
        if  path.exists(archivo_maze) and path.exists (archivo_problem):
            a=Laberinto(archivo_maze,archivo_problem)
        else: 
            print("Uno de los ficheros no son validos ")
    elif archivo_maze is None and filas is None and columnas is None:
        print("??le gustaria trabajar con un archivo? Si/No\n")
        opcion=str(input('>>'))
        opcion=opcion.upper()
        if opcion == 'SI':
            print('Introduzca un nombre de fichero laberinto\n')
            fichero_laberinto=str(input('>>'))
            print('Introduzca un nombre de fichero problema\n')
            fichero_problema=str(input('>>'))
            if  path.exists(fichero_laberinto) and path.exists (fichero_problema):
                a=Laberinto(fichero_laberinto,fichero_problema)
            else: 
                print("Uno de los ficheros no son validos ")
        if opcion =='NO':
            print('Introduzca filas\n')
            filas=int(input('>>'))
            print('Introduzca columnas\n')
            columnas=int(input('>>'))
            
            a=Laberinto(filas,columnas)
    elif filas is not None and columnas is not None:
        a=Laberinto(filas,columnas)       
    else:
        print (" Introduzca los dos atributos  , ponga -h para mas informacion")
    

main()
