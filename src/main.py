import io
from fastapi.responses import HTMLResponse
from scripts import MetricsV4 as cm
from fastapi import FastAPI, UploadFile, HTTPException, File, Form, status
from pathlib import Path
import json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import HTMLResponse
import fitz
import logging
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader, PdfWriter
import magic
from typing import Annotated
from fastapi.staticfiles import StaticFiles
#Configuración de logging
logger=logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app = FastAPI() #objeto que instancia Fast API



#SEGURIDAD PERIMETRAL

#Configuración del tamaño de PDF
MAX_FILE_SIZE = 4 * 1024 * 1024  # 10MB límite de tamaño
ALLOWED_MIME_TYPES = {"application/pdf"}

#Configuración para la optimización

#Validar tamaño del documento
async def validate_file_size(file:UploadFile) -> None:
     file.file.seek(0,2)#Ir al final del archivo
     file_size = file.file.tell()
     file.file.seek(0)

     if file_size > MAX_FILE_SIZE:
          raise HTTPException(
               status_code= status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
               detail = f"El archivo excede el tamaño máximo permitido de {MAX_FILE_SIZE} bytes"
          )
#Validar tipo de documento
async def validate_pdf_file(file:UploadFile) -> bytes:
     #Leer los primeros bytes sea un PDF
     content = await file.read(2048)
     file_type = magic.from_buffer(content, mime=True)

     if file_type not in ALLOWED_MIME_TYPES:
          raise HTTPException(
               status_code= status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
               detail="El archivo debe ser un PDF válido"
          )
     
     #Leer el resto del archivo
     remaining_content = await file.read()
     full_content = content + remaining_content
     file.file.seek(0)

     return full_content
     
def sanitize_pdf(content: bytes) -> bytes:
     #Eliminar metadaos potencialemente maliciosos del PDF

     try:
          reader = PdfReader(io.BytesIO(content))
          writer = PdfWriter()

          for page in reader.pages:
               writer.add_page(page)

     #Eliminando metadatos
          writer.add_metadata({})

          output = io.BytesIO()
          writer.write(output)
          return output.getvalue()
     
     except Exception as e:
          logger.error(f"Error en sanitización de PDF: {str(e)}")
          raise HTTPException(
               status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
               detail="El PDF no pudo ser procesado por contener contenido inválido"
          )


def extract_text_from_pdf(content: bytes) -> str:
     "Extracción de texto de un PDF"
     try:
          doc = fitz.open(stream=content, filetype="pdf")
          text = ""
          for page in doc:
               text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
          
          return text

     except Exception as e:
          logger.error(f"Error al extraer texto del PDF: {str(e)}")
          raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El PDF no pudo ser procesado y no se pudo extraer el texto"
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/static", 
    StaticFiles(directory=str(Path(__file__).resolve().parent.parent / "static")), 
    name="static"
)

@app.get("/", response_class= HTMLResponse)
async def root():
    """Servir interfaz principal"""
    try:
        with open(Path(__file__).resolve().parent.parent / "static" / "index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not found")


@app.post("/metrics")
async def metrics(metric: Annotated[str, Form(description= "Métrica a calcular: lexical_density, sophistication, ttr, root_ttr, ttr_corrected, flesh, kincaid, fog, smog")], file:Annotated[UploadFile, File(description="Archivo PDF a analizar")]):
     try:
          
          await validate_file_size(file)
          file_content = await validate_pdf_file(file)
          sanitize_content = sanitize_pdf(file_content)
          text = extract_text_from_pdf(sanitize_content)
          metric = metric.lower()
          
        
          if metric == "lexical_density":

               current_document = cm.calculateLexicalDensity(text)
               with open("./JSON_Metrics/Lexical_density.json", "r") as file:
                    data = json.load(file)
                    data['metric'] = "Lexical_Density"
                    data['current_document'] = current_document
               del text
               return data
          
          elif metric =="sophistication":

               current_document=cm.calculateSophistication(text)
               with open("./JSON_Metrics/Sophistication.json", "r") as file:
                    data = json.load(file)
                    data['metric'] = "Sophistication"
                    data['current_document']= current_document 
               del text
               return data
          

          elif metric =="ttr":

               current_document=cm.calculateTTR(text)
               with open("./JSON_Metrics/TTR.json", "r") as file:
                    data = json.load(file)
                    data['metric'] = "TTR"
                    data['current_document']= current_document 
               del text
               return data
          
          elif metric == "root_ttr":

               current_document=cm.calculateTTRRoot(text)
               with open("./JSON_Metrics/Root_TTR.json","r") as file:
                    data = json.load(file)
                    data['metric'] = "RootTTR"
                    data['current_document']= current_document
               del text
               return data

          elif metric == "ttr_corrected":

               current_document = cm.calculateTTRCorrected(text)
               with open("./JSON_Metrics/Corrected_TTR.json","r") as file:
                    data = json.load(file)
                    data['metric'] = "CorrectedTTR"
                    data['current_document']= current_document
               del text
               return data
          
          
          elif metric == "flesh":

               current_document = cm.TFRE(text)
               with open("./JSON_Metrics/Flesh.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The Flesh Reading Ease Score"
                    data["current_document"] = current_document
               del text
               return data

          elif metric == "kincaid":

               current_document = cm.TFREK(text)
               with open("./JSON_Metrics/Flesh_Kincaid.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The Flesh-Kincaid Reading Ease Score"
                    data["current_document"] = current_document
               del text
               return data
          
          elif metric == "fog":

               current_document = cm.FogIndex(text)
               with open("./JSON_Metrics/FogIndex.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The Fog Index"
                    data["current_document"] = current_document
               del text
               return data
          
          elif metric == "smog":

               current_document = cm.SMOG(text)
               with open("./JSON_Metrics/SMOG.json","r") as file:
                    data = json.load(file)
                    data["metric"]="The SMOG Index"
                    data["current_document"] = current_document
               del text
               return data

          else:
               raise HTTPException(status_code=400, detail="Metric not supported")
          
     except HTTPException as he:
          raise he
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
     
     finally:
          #Limpieza de memoria
          # Liberar explícitamente variables grandes
        if file_content is not None:
            del file_content
        if sanitize_content is not None:
            del sanitize_content

        
        # Forzar recolección de basura
        import gc
        gc.collect()




    

@app.post("/prediction")
async def predicitve_model(file:Annotated[UploadFile, File(description="Archivo PDF a analizar")]):
     
     try:
          await validate_file_size(file)
          file_content = await validate_pdf_file(file)
          sanitize_content = sanitize_pdf(file_content)
          text = extract_text_from_pdf(sanitize_content)

          text= cm.removeReferences(text)
          text= cm.cleanText(text)

          prediction = {
               "prediction": cm.prediction(text)[0]
          }

          return prediction
     
     except HTTPException as he:
          raise he
     except Exception as e:
          logger.exception("Error processing the PDF file")
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
          






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)