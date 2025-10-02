#En este archivo se experimenta para crear, leer y modificar un archivo JSON
import json

path= "D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/Code/Manejo_JSON/ArchivoJSON.json"#ruta del archivo JSON a 


#crear un archivo JSON a partir de un diccionario de datos de python
"""
data={
      "nombre":"Cesar",
      "edad":21,
      "pais":"Mexico",
      "estado":"Hidalgo",
      "municipio":"pachuca",
      "gustos":["videojuegos","autos", "motos","aviones"] 
      }

"""
"""
with open(path, "w", encoding="utf-8") as file:
    json.dump(data,file)#aqui se toma la cadena de
    file.close()

"""
#Abrir el JSON y convertir su contenido en un diccionario de Python
"""
with open(path,"r") as file:
    data=json.load(file)
    print(data)
    print(type(data))
"""

#Abrir el JSON y mostrar su contenido como una cadena que cumple con las reglas de formato de JSON(no es muy correcto pero para fines didacticos se hizo de esta forma)
"""
with open(path,"r") as file:
    data=json.load(file)
    print(data)
    print(type(data))
    data=json.dumps(data)
    print(data)
    print(type(data))
"""

"Abrir y modificar parametros y agregar nuevo para después guardarlo en un JSON"
"""
with open(path,"r") as file:
    data=json.load(file)
    print(data)
    print(type(data))
    
    data["nombre"]="Oscar"
    data["edad"]="34"
    data["gustos"][1]="barcos"
    data["comida_favorita"]="pizza"
    
    with open(path,"w", encoding="utf-8") as file:
        json.dump(data, file)
"""

#mostrar los cambios
with open(path,"r") as file:
    data=json.load(file)
    print(data)
    print(type(data))



   