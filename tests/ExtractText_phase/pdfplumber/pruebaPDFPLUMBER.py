import pdfplumber

import os

pdfs="D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/PDFs/" #En caso de estar en otra carpeta se debe poner la ruta, rb= lectura en binario

langFile = os.listdir(pdfs)#Lista de nombres de archivos dentro de la carpeta
file=""

for file in langFile:
    print(file)
    file_path = os.path.join(pdfs,file)#se junta tanto la dirección de carpeta como el nombre del archivo
    pdf=open(file_path,"rb")
    print(pdf)
    
    with pdfplumber.open(pdf) as pdfLeer:
        
        text=""
        for page in pdfLeer.pages:
            
            text+=page.extract_text()
            print("dentro de for de paginas")#bandera
        
        decoded_text= text.encode('utf-8',errors='ignore').decode('utf-8',errors='ignore')
        #En esta línea de toma el texto leido del pdf y se convierte las cadenas de texto en bytes siguiendo el formato
        #utf-8 representando secuencias binarias siguiendo este estandar.
        #Para poder poner el texto en un txt se tiene que pasar los bytes a texto entonces de decodifica usando el estandar utf-8, nuevamente
            
            
        with open("D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/Txt's-Pdfplumber/"+file +"-pdfplumber.txt","w", encoding="utf-8") as txt: 
            print("agregando al txt")
            txt.write(decoded_text)
            txt.close()


