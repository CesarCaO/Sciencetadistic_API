
from Metrics_Versions import MetricsV4 as cm
from fastapi import FastAPI, UploadFile, HTTPException
import json
import fitz
import logging

#Configuración de logging
logger=logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app = FastAPI() #objeto que instancia Fast API


#Configuración de seguridad
#MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB límite de tamaño
#ALLOWED_MIME_TYPES = {"application/pdf"}




@app.post("/metrics")
def metrics(metric: str, file: UploadFile):
     try:
          metric = metric.lower()
          file.file.seek(0)  # Reset the file pointer to the beginning
          doc = fitz.open(stream=file.file.read(), filetype="pdf")
          text = ""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
          
        
          if metric == "lexical_density":

               current_document = cm.calculateLexicalDensity(text)
               with open("./JSON_Metrics/Lexical_Density.json", "r") as file:
                    data = json.load(file)
                    data['metric'] = "Lexical_Density"
                    data['current_document'] = current_document
               return data
          
          elif metric =="sophistication":

               current_document=cm.calculateSophistication(text)
               with open("./JSON_Metrics/Sophistication.json", "r") as file:
                    data = json.load(file)
                    data['metric'] = "Sophistication"
                    data['current_document']= current_document 
               return data
          

          elif metric =="ttr":

               current_document=cm.calculateTTR(text)
               with open("./JSON_Metrics/TTR.json", "r") as file:
                    data = json.load(file)
                    data['metric'] = "TTR"
                    data['current_document']= current_document 
               return data
          
          elif metric == "root_ttr":

               current_document=cm.calculateTTRRoot(text)
               with open("./JSON_Metrics/Root_TTR.json","r") as file:
                    data = json.load(file)
                    data['metric'] = "RootTTR"
                    data['current_document']= current_document
               return data

          elif metric == "ttr_corrected":

               current_document = cm.calculateTTRCorrected(text)
               with open("./JSON_Metrics/Corrected_TTR.json","r") as file:
                    data = json.load(file)
                    data['metric'] = "CorrectedTTR"
                    data['current_document']= current_document
               return data
          
          
          elif metric == "flesh":

               current_document = cm.TFRE(text)
               with open("./JSON_Metrics/Flesh.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The Flesh Reading Ease Score"
                    data["current_dcoument"] = current_document
               return data

          elif metric == "kincaid":

               current_document = cm.TFREK(text)
               with open("./JSON_Metrics/Kincaid.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The Flesh-Kincaid Reading Ease Score"
                    data["current_dcoument"] = current_document
               return data
          
          elif metric == "fog":

               current_document = cm.FogIndex(text)
               with open("./JSON_Metrics/FogIndex.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The Fog Index"
                    data["current_dcoument"] = current_document
               return data
          
          elif metric == "smog":

               current_document = cm.SMOG(text)
               with open("./JSON_Metrics/SMOG.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The SMOG Index"
                    data["current_dcoument"] = current_document
               return data

          else:
               raise HTTPException(status_code=400, detail="Metric not supported")
          

     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))


     raise HTTPException(status_code=500, detail=str(e))  

@app.post("/model/")
def predicitve_model(file: UploadFile):

     try:
          file.file.seek(0)  # Reset the file pointer to the beginning
          doc = fitz.open(stream=file.file.read(), filetype="pdf")
          text = ""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
          
          text = cm.removeReferences(text)
          text = cm.cleanText(text)

          x_test=[text.lower()]
     
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))

