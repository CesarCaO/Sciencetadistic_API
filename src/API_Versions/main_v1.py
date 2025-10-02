import scripts.MetricsV4 as cm
from fastapi import FastAPI, UploadFile, HTTPException
import json
import fitz
import logging


logger=logging.getLogger("uvicorn.error")
app = FastAPI() #objeto que instancia Fast API

@app.post("/tagged_lexical_density/")
def tagged_lexical_density_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          tagged_lexical_density=m.calculateTaggedLexicalDensity(text)#*

          with open("./JSON_Metrics/Lexical_density.json", "r") as file:
               data=json.load(file)

               data['current_document']=tagged_lexical_density#*

          return data

     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))  


@app.post("/sophitication/")
def sophitication_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          sophitication=m.calculateSophistication(text)

          with open("./JSON_Metrics/Lexica_density.json", "r") as file:
               data=json.load(file)
               data['current_document']=sophitication

          return data

     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

@app.post("/sophitication_by_lenght/")
def sophitication_by_lenght_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          sophitication_by_lenght=m.calculateSophisticationByLenght(text)

          with open("./JSON_Metrics/Lexical_density.json", "r") as file:
               data=json.load(file)
               data['current_document']=sophitication_by_lenght

          return data

     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

@app.post("/ttr_tagged/")
def ttr_tagged_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          ttr_tagged=m.calculateTTRTagged(text)

          with open("./JSON_Metrics/Lexical_density.json", "r") as file:
               data=json.load(file)
               data['current_document']=ttr_tagged

          return data

     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))
#Implement the others metrics



@app.post("/ttr_root/")
def ttr_root_document(file:UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          ttr_root=m.calculateTTRRoot(text)
          with open("./JSON_Metrics/Lexical_density.json","r") as file:
               data=json.load(file)
               data["current_document"]=ttr_root
          return data
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

@app.post("/ttr_corregido/")
def ttr_corregido_document(file : UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          ttr_corregido=m.calculateTTRCorregido(text)
          with open("./JSON_Metrics/Lexical_density.json","r") as file:
               data=json.load(file)
               data["current_document"]=ttr_corregido
          return data
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

#*Readability metrics

@app.post("/tfre/")
def tfre_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          tfre=m.TFRE(text)
          with open("./JSON_Metrics/Lexical_density.json","r") as file:
               data=json.load(file)
               data["current_document"]=tfre
          return data
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

@app.post("/The_Flesch_Kincaid/")
def the_flesch_kincaid_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          the_flesch_kincaid=m.The_Flesch_Kincaid(text)
          with open("./JSON_Metrics/Lexical_density.json","r") as file:
               data=json.load(file)
               data["current_document"]=the_flesch_kincaid
          return data
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

@app.post("/the_fog_index/")
def the_fog_index_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          the_fog_index=m.The_Fog_Index(text)
          with open("./JSON_Metrics/Lexical_density.json","r") as file:
               data=json.load(file)
               data["current_document"]=the_fog_index
          return data
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

@app.post("/smog_index/")
def the_smog_index_document(file: UploadFile):
     try:
          file.file.seek(0)
          doc= fitz.open(stream=file.file.read(), filetype="pdf")
          text=""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

          the_smog_index=m.The_SMOG_Index(text)
          with open("./JSON_Metrics/Lexical_density.json","r") as file:
               data=json.load(file)
               data["current_document"]=the_smog_index
          return data
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))