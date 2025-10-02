from bs4 import BeautifulSoup
import json
import os



path="D:/Proyectos Spyder/Categorizador de documentos/parsed/"

xmls="D:/Proyectos Spyder/Categorizador de documentos/Grobid_resultados/"

langFile=os.listdir(xmls)

xml_file=""



for f in langFile:
    filename=os.path.join(xmls, f)
    
    with open(filename, 'r',encoding="utf-8") as xml:
        documento={
            
                "titulo":"",#ya se puede recuperar
                "autores":[],
                "editorial":"",
                "abstract":[],
                "contenido":[],
                "referencias":[]
                
                
            }
        root=BeautifulSoup(xml,"lxml-xml")
        
        
        
        
        sourceDesc=root.find("sourceDesc")#guarda el primer nodo encontrado con el mismo nombre
        
        titulo=sourceDesc.find('title').text
        
        documento["titulo"]=titulo
        
        autores=sourceDesc.find_all("author")
        
        for autor in autores:
            nuevo_autor={}
            first_forename=autor.find_all("forename", type="first")
            middle_forename=autor.find_all("forename", type="middle")
            surname=autor.find_all("surname")
            orcid=autor.find_all("idno")
            
            for first in first_forename:
                print("Primer Nombre "+first.text)
                nuevo_autor["primerNombre"]=first.text
            for middle in middle_forename:
                print("Segundo Nombre "+middle.text)
                nuevo_autor["segundoNombre"]=middle.text
            for sur in surname:
                print("Apellidos "+sur.text)
                nuevo_autor["apellidos"]=sur.text
            for x in orcid:
                print("ORCID "+x.text)
                nuevo_autor["ORCID"]=x.text
            
            if any(nuevo_autor.values()):
                documento["autores"].append(nuevo_autor)
            
        editorial=""
        if(sourceDesc.find('publisher')):
            editorial=sourceDesc.find('publisher').text
    
        documento["editorial"]=editorial
        abstract=root.find("abstract")
        
        head=abstract.find_all("div")
        
        for resumen in head:
            abstract_text={}
            header=""
            if(resumen.find("head")):
                header=resumen.find("head")
                abstract_text["header"]=header.text
            texto=resumen.find_all("p")
            abstract_text["text"]=[]
            for p in texto:
                abstract_text["text"].append(p.text)
                
            documento["abstract"].append(abstract_text)
            
        text=root.find("text")
        body=text.find("body")
        div=body.find_all("div")
        
        for content in div:
            nuevo_contenido={}
            titulos=content.find("head")
            #print(titulos.text)
            nuevo_contenido["titulos"]=titulos.text
            texto=content.find_all("p")
            nuevo_contenido["text"]=[]
            
            for p in texto:
                #print(p.text)
                nuevo_contenido["text"].append(p.text)
            
            documento["contenido"].append(nuevo_contenido)
        
        back=root.find("back")
        references=back.find("div", type="references")
        listBibl=references.find_all("listBibl")
        
        for referencia in listBibl:
            nueva_referencia={}
            biblStruct=referencia.find_all("biblStruct")
            
            for x in biblStruct:
                
                title=x.find("title")
                #print(title.text)
                nueva_referencia={"titulo":title.text}
                
                ref_autores=x.find_all("author")
                
                for author in ref_autores:
                    first_forename=author.find_all("forename", type="first")
                    middle_forename=author.find_all("forename", type="middle")
                    surname=author.find_all("surname")
                    
                    
                    for first in first_forename:
                        #print("Primer Nombre "+first.text)
                        nueva_referencia["primerNombre"]=first.text
                    for middle in middle_forename:
                        #print("Segundo Nombre "+middle.text)
                        nueva_referencia["segundoNombre"]=middle.text
                    for sur in surname:
                        #print("Apellidos "+sur.text)
                        nueva_referencia["apellidos"]=sur.text
                    
                note=x.find("note", type="raw_reference")
                
                #print(note.text)
                nueva_referencia["raw_reference"]=note.text
                
                if any(nueva_referencia.values()):
                    documento["referencias"].append(nueva_referencia)
                
       # print(documento)
        
        with open(path+f+".json","w",encoding="utf-8") as file:
            json.dump(documento,file, ensure_ascii=False,indent=4)#Se esta 
            file.close()
         

    
        
   
        
        
  
    
    
    

    
        
    
    #¿Como puedo separar los nombres en primer nombre, segundo, apellidos y ORCID-ID?
    
    
        
        
       
        
