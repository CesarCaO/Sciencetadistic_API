import nltk
import spacy

nltk.download('punkt', quiet=True)
spacy.cli.download("en_core_web_sm")


import Metrics as m
spacy.require_cpu()
npl = spacy.load("en_core_web_sm", disable=["parser", "ner"])

from fastapi import FastAPI, UploadFile, HTTPException
import json
import fitz
import logging


logger=logging.getLogger("uvicorn.error")
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
     try:
          file.file.seek(0)  # Reset the file pointer to the beginning
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
          
          lexical_density=m.calculateLexicalDensity(text)

          with open("./JSON_Metrics/Lexical_density.json", "r") as file:
               data=json.load(file)
               data['current_document']=lexical_density
               
          return data
     
     except Exception as e:

          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))
     
 
