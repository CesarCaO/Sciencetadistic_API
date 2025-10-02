import pdfplumber
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
    
    with pdfplumber.open(pdf) as pdfLeer:
        
        
        tables=[]
        for page in pdfLeer.pages:
            
            table=page.extract_table()
            
            if(table):
                tables.append(table)
            
    
    if(tables):
        output_path = f"D:/Documentos HDD/Proyectos Spyder/Categorizador de documentos/Tablas-Pdfplumber/{file}-Tablas-pdfplumber.txt"
        
        with open(output_path,"w", encoding="utf-8") as txt:
        
            for table in tables:
                    print("agregando al txt")
                    #Agregando el formato tabular (a estudiar)
                    table_text = "\n".join(["\t".join(celda if celda is not None else "" for celda in row) for row in table if row])  # Formato tabular
                    txt.write(table_text + "\n\n")

