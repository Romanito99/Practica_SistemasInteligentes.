

class Nodo(object):
    def __init__(self,id,costo,id_estado,id_padre,accion,profundidad,heuristica,valor):
        self.id=id
        self.costo=costo
        self.id_estado=id_estado
        self.id_padre=id_padre
        self.accion=accion
        self.profundidad=profundidad
        self.heuristica=heuristica
        self.valor=valor

    def set_id(self,id):
        self.id=id
    def set_costo(self,c):
        self.costo=c
    def set_id_estado(self,e):
        self.id_estado=e
    def set_id_padre(self,p):
        self.id_padre=p
    def set_accion(self,a):
        self.accion=a
    def set_profundidad(self,p):
        self.profundidad=p
    def set_heuristica(self,h):
        self.heuristica=h
    def set_valor(self,v):
        self.valor=v

    def get_id(self):
        return self.id
    def get_costo(self):
        return self.costo
    def get_id_estado(self):
        return self.id_estado
    def get_id_padre(self):
        return self.id_padre
    def get_accion(self):
        return self.accion
    def get_profundidad(self):
        return self.profundidad
    def get_heuristica(self):
        return self.heuristica
    def get_valor(self):
        return self.valor