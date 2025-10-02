import fitz
import os


pdfs="D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/PDFs/"

langFile = os.listdir(pdfs)#Lista de nombres de archivos dentro de la carpeta
file=""
tables=[]

for file in langFile:
    print(file)
    file_path = os.path.join(pdfs,file)#se junta tanto la dirección de carpeta como el nombre del archivo
    pdf=open(file_path,"rb")
    print(pdf)
    
    doc=fitz.open(pdf)
    
    for page_index in range(len(doc)):#iterar en llas paginas de los pdf
        page=doc[page_index]#obtener la pagina
        image_list=page.get_images()
        
        #PyMuPDF cuenta con metodos especiales para los objetos de tipo documento uno de ellos es _getitem_(self,index) que permite acceder a las
        #paginas o elementos mediante indices.
        
        #imprimir el numero de paginas encontradas
        if image_list:
            print(f"Se encontraron {len(image_list)} imagenes en la pagina {page_index} ")
        else:
            print("No se encontró ninguna imagen", page_index)
            
            
        for image_index, img in enumerate(image_list, start=1):
            xref=img[0]#XREF es un numero entero asignado a cada objeto de un archivo PDF
            pix=fitz.Pixmap(doc, xref)
            
            if pix.n - pix.alpha>3:#CMYK: Convertir a RGB primero
                pix=fitz.Pixmap(fitz.csRGB,pix)
            
            pix.save("D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/Imagenes-PyMuPDF/"+file+" page_%s-image%s.png" % (page_index,image_index))
            pix=None
