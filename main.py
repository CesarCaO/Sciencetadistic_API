from fastapi import FastAPI
import json

app = FastAPI() #objeto que instancia Fast API

@app.get("/")#Cuando alguien llame a ala ruta raíz entonces haz lo que viene en la línea inmediata
def index():
     return {"saludo": "HOLA MUNDO"} #fast api ya jsonifica el retorno

@app.post("/title_size")
def title_size():
     with open("./JSON_Metrics/Title_size.json", "r") as file:
          data=json.load(file)
          data['current_document']=17
     return data
