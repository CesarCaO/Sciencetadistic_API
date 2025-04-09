from fastapi import FastAPI

app = FastAPI() #objeto que instancia Fast API

@app.get("/")#Cuando alguien llame a ala ruta raíz entonces haz lo que viene en la línea inmediata
def index():
     return {"saludo": "Hola fokin mundo"} #fast api ya jsonifica el retorno