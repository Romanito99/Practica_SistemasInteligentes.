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
        
    def creacion_sucesores(self,estados):
        funcion_sucesores=[]
        sucesores=[]
        for i in estados:
            f,c = i.get_tupla()
            if f==0:
                if i.get_N()==True:
                    
                    
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
            funcion_sucesores.append(sucesores)
        return funcion_sucesores


        

    def generar_estados(self, casillas):
        estados=[]
        for i in casillas:
            tupla=i.get_tupla()
            valor=i.get_valor()
            estado=Estado(tupla,valor)
            estados.append(estado)
        return estados


