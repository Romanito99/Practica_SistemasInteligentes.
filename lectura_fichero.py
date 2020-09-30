import json

with open("fichero.json") as f:
    datos=f.read()
datos=json.loads(datos)
rows=datos["rows"]
cols=datos["cols"]
max_n=datos["max_n"]
mov=datos["id_mov"]
cells=datos["cells"]

for entity in cells:
    entityName = entity
    value=cells[entityName]["value"]
    neighbors=cells[entityName]["neighbors"]
    print(value)
    print(neighbors)

    