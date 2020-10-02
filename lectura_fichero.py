import json
class Lectura_ficheros():
    def leer_json(self):
        with open("fichero.json") as f:
            datos=f.read()
        datos=json.loads(datos)
        rows=datos["rows"]
        cols=datos["cols"]
        max_n=datos["max_n"]
        mov=datos["mov"]
        id_mov=datos["id_mov"]
        cells=datos["cells"]
        lista_values=[]
        lista_neighbours=[]
        for entity in cells:
            entityName = entity
            print(entity)
            value=cells[entityName]["value"]
            neighbors=cells[entityName]["neighbors"]
            lista_values.append(value)
            lista_neighbours.append(neighbors)


    
b=Lectura_ficheros()
b.leer_json()