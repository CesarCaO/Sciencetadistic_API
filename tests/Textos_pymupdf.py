import fitz
import os
import nltk
from scripts import MetricsV4 as cm
"""
pdfs="D:/Proyectos Spyder/Categorizador de documentos/PDFs/" #En caso de estar en otra carpeta se debe poner la ruta, rb= lectura en binario

langFile = os.listdir(pdfs)#Lista de nombres de archivos dentro de la carpeta
file=""

for file in langFile:
    print(file)
    file_path = os.path.join(pdfs,file)#se junta tanto la dirección de carpeta como el nombre del archivo
    pdf=open(file_path,"rb")
    
    doc = fitz.open(pdf)
    
    text=""
    
    for page in doc:
        
        text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
        
    with open("D:/Proyectos Spyder/Categorizador de documentos/Txt-pymupdf/"+file +".txt","w", encoding="utf-8") as txt: 
        print("agregando al txt")
        txt.write(text)
        txt.close()
"""

pdf= "./PDFs/test_papers/Accepted/REPORTE DE CONFERENCIA (MECANICA DE SUELOS).pdf"

doc = fitz.open(pdf, filetype="pdf")
text = ""
for page in doc:
    text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

#text=cm.removeReferences(text)
#text=cm.cleanTextForMetrics(text)
print("número de oraciones: ", len(nltk.sent_tokenize(text)) )
#print(text)