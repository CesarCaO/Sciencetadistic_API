
from functools import lru_cache
from typing import Dict
import MetricsV3 as cm
from fastapi import Depends, FastAPI, Path, UploadFile, HTTPException
import json
import fitz
import logging


logger=logging.getLogger("uvicorn.error")

class JSONTemplateManager:
     def __init__(self, template_path: str = "./JSON_Metrics"):
          self.templeate_path = Path(template_path)
          self._templates = None

     @lru_cache()
     def get_templates(self) -> Dict[str, Dict]:
          if self._templates is None:
               templates={}
               template_files={
                    "ttr": "TTR.json",
                    "root_ttr": "Root_TTR.json", 
                    "ttr_corrected": "Corrected_TTR.json",
                    "flesh": "Flesh.json"
               }

               for key, filename in template_files.items():
                    try:
                         with open(self.template_path / filename, "r") as file:
                              templates[key] = json.load(file)
                    except FileNotFoundError:
                         logger.warning(f"Plantilla {filename} not found")
                         templates[key] = {"metric": key, "error": "Template not found"}
          
               self._templates = templates
          return self._templates


template_manager = JSONTemplateManager(template_path="./JSON_Metrics")
app = FastAPI() #objeto que instancia Fast API


#Para mantere la API sin estado, como lo dictamina las reglas de creación de una API REST hay que cargar los JSON una sola vez y mantenerlos en memoria


@app.post("/metrics")
def metrics(metric: str, file: UploadFile, templates: Dict[str, Dict] = Depends(template_manager.get_templates)):
     try:
          metric = metric.lower()
          file.file.seek(0)  # Reset the file pointer to the beginning
          doc = fitz.open(stream=file.file.read(), filetype="pdf")
          text = ""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
          
          if metric not in templates:
               raise HTTPException(status_code= 400, detail=f"Metric not supported")

          if metric =="ttr":

               current_document=cm.calculateTTR(text)
              
          
          elif metric == "root_ttr":

               current_document=cm.calculateTTRRoot(text)
              

          elif metric == "ttr_corrected":

               current_document = cm.calculateTTRCorrected(text)
               
          
          elif metric == "flesh":

               current_document = cm.TFRE(text)
               
          
          else:
               raise HTTPException(status_code=400, detail="Metric not supported")
          
          response_data = templates[metric].copy()
          response_data['current_document'] = current_document
          
          return response_data

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

