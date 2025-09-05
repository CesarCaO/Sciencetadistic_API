
import MetricsV3 as cm
from fastapi import FastAPI, UploadFile, HTTPException
import json
import fitz
import logging


logger=logging.getLogger("uvicorn.error")
app = FastAPI() #objeto que instancia Fast API


@app.post("/metrics")
def metrics(metric: str, file: UploadFile):
     try:
          metric = metric.lower()
          file.file.seek(0)  # Reset the file pointer to the beginning
          doc = fitz.open(stream=file.file.read(), filetype="pdf")
          text = ""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
          

          if metric =="ttr":

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
          
          else:
               raise HTTPException(status_code=400, detail="Metric not supported")
          

     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=500, detail=str(e))


"""
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
"""
@app.post("/ia_model/")
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

