import fitz
import os

pdfs="D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/PDFs/" #En caso de estar en otra carpeta se debe poner la ruta, rb= lectura en binario
langFile = os.listdir(pdfs)#Lista de nombres de archivos dentro de la carpeta
file=""

for file in langFile:
    print(file)
    file_path = os.path.join(pdfs,file)#se junta tanto la dirección de carpeta como el nombre del archivo
    pdf=open(file_path,"rb")
    
    doc=fitz.open(pdf)
    
    for page in doc:
        
        tabs=[]
        
        tabs=page.find_tables()
        
        if tabs.tables:
            print(tabs[0].extract())
        
        
        
     



