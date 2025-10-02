import json


"""
#primer uso de un JSON

#Cadena en Formato JSON a un diccionario de dato de Python
json_str='{"nombre":"Cesar","edad":21,"pais":"México"}'#"llave":"valor", cadena de caracteres que cumple con la regla de formato JSON

#todo el contenido entre llaves representa el conjunto de pares y valores que se va contener dentro de la estructura

python_dict=json.loads(json_str)# conviertes una cadena en un formato JSON a una estructura de dato de PYTHON

print(type(python_dict))

#aqui se esta mostrando los atributos del diccionario (objeto) python_dict
print(python_dict['nombre'])
print(python_dict['edad'])
print(python_dict['pais'])

"""

#De un diccionario de datos a un JSON
#diccionario de datos
data={
      "nombre":"juanito",
      "edad":105,
      "pais":"alaska",
      "leguajes":["PHP","Python","Java","JavaScript", "C#"]#lista en python
      }


json_data=json.dumps(data)#esta funcion toma un diccionario de datos de Python y devuelve una cadena de caracteres que cumple con el formato JSON
print(json_data)
print(type(json_data))


"""


Equivalencia de tipos de datos
Python ||  JSON

dict  =>  Object
list  =>  Array
tuple =>  Array
str   =>  String
int   =>  Number
float =>  Number
True  =>  true
False =>  false
None  =>  null
"""
"""
data={#diccionario de datos
      "nombre":"juanito",
      "edad":105,
      "pais":"alaska",
      "leguajes":["PHP","Python","Java","JavaScript", "C#"]#lista en python
      }
"""
#json_data=json.dumps(data, indent=4, separators=(",",":"))
#json_data=json.dumps(data, indent=4, separators=(",",":"), sort_keys=True)
#print(json_data)

#load= cargar desde JSON un diccionario de datos
#dumps= apartir de un diccionario de datos crear un JSON o pasarlo a un str
"""
json_data=json.JSONEncoder().encode({"lenguajes":["Python", "JavaScript"]})
print(json_data)
print(type(json_data))
python_dcit=json.JSONDecoder().decode(json_data)
print(python_dcit)
print(type(python_dcit))
"""

    
  
  

        


