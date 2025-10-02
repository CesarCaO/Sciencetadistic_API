

import PyPDF2 
import os

#Los PDF estan en binario
#Se declara una variable con la que se abre el objeto
pdfs="D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/PDFs/" #En caso de estar en otra carpeta se debe poner la ruta, rb= lectura en binario

langFile = os.listdir(pdfs)#Lista de nombres de archivos dentro de la carpeta
file=""

for file in langFile:
    print(file)
    file_path = os.path.join(pdfs,file)#se junta tanto la dirección de carpeta como el nombre del archivo
    pdf=open(file_path,"rb")
    
    reader=PyPDF2.PdfReader(pdf)
   
    for page in range(len(reader.pages)):#iterador en un rango del número de paginas
        
        imgPage=reader._get_page(page)
        
        for image_file_object in imgPage.images:
            with open("D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/Images-PyPDF2/"+file+"_pypdf_"+image_file_object.name, "wb") as fp:
                fp.write(image_file_object.data)#para poder generar imagenes se necesitan valores binarios
                fp.close()
