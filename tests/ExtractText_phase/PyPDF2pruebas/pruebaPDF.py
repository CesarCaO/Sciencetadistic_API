
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

    
    
    
    reader=PyPDF2.PdfReader(pdf)#variable que guarda la dirección de un objeto
    numPage=len(reader.pages) #obteniendo el número de paginas del documento
    
    extract_info=""#inicializar extract a null

    for page in range(numPage):#iterador en un rango del número de paginas
        
        print("dentro de for range")#bandera
        info= reader._get_page(page)
        extract_info += info.extract_text() #Para poder concatenar hay que inicializar antes
        
       
        
    
    decoded_text= extract_info.encode('utf-8',errors='ignore').decode('utf-8',errors='ignore')
    #En esta línea de toma el texto leido del pdf y se convierte las cadenas de texto en bytes siguiendo el formato
    #utf-8 representando secuencias binarias siguiendo este estandar.
    #Para poder poner el texto en un txt se tiene que pasar los bytes a texto entonces de decodifica usando el estandar utf-8, nuevamente
        
        
    
    with open("D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/Txt's-PyPDF/"+file +"-pypdf.txt","w", encoding="utf-8") as txt: 
        txt.write(decoded_text)
        txt.close()
        
   
        

