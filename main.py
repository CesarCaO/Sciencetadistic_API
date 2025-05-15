from fastapi import FastAPI, UploadFile
import json
import fitz
import Metrics as m

app = FastAPI() #objeto que instancia Fast API

@app.get("/")#Cuando alguien llame a ala ruta raíz entonces haz lo que viene en la línea inmediata
def index():
     return {"saludo": "HOLA MUNDO"} #fast api ya jsonifica el retorno

@app.get("/title_size")
def title_size():
     with open("./JSON_Metrics/Title_size.json", "r") as file:
          data=json.load(file)
          data['current_document']=17
     return data

@app.post("/lexical_density/")
def tittle_size_document(file: UploadFile):
     pdf=open(file.file,"rb")
     doc=fitz.open(pdf)
     text=""
     for page in doc:
          text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
     
     lexical_density=m.calculateLexicalDensity(text)

     with open("./JSON_Metrics/Lexical_density.json", "r") as file:
          data=json.load(file)
          data['current_document']=lexical_density
          
     return data
     
 
