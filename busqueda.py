import json
from estado import Estado
from casilla import Casilla
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
        
    def creacion_sucesores(self,estado,numero,filas,columnas):
        f,c =estado.get_tupla()
        funcion_sucesores=[]
        sucesores=[]

        if (f==0):
            sucesores=['S', (f+1,c), 1] 
            funcion_sucesores.append(sucesores)
        elif (f==filas-1):
            sucesores=['N', (f-1,c), 1] 
            funcion_sucesores.append(sucesores) 
        else:
            sucesores=['N', (f-1,c), 1]
            funcion_sucesores.append(sucesores) 
            sucesores=['S', (f+1,c), 1] 
            funcion_sucesores.append(sucesores)

        if (c==0):
            sucesores=['O', (f,c+1), 1]
            funcion_sucesores.append(sucesores)
        elif (c==columnas-1):
            sucesores=['E', (f,c-1), 1]
            funcion_sucesores.append(sucesores)
        else:
            sucesores=['O', (f,c+1), 1]
            funcion_sucesores.append(sucesores)
            sucesores=['E', (f,c-1), 1]
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


