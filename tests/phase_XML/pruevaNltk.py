import json

import nltk

path="D:/Proyectos Spyder/Categorizador de documentos/parsed/Clasificacion_de_opiniones_provenientes.xml.json"

with open(path,"r", encoding="utf-8") as file:
    documento=json.load(file)
    
    #print(documento)
    
    numeroReferencias=len(documento["referencias"])
    
    print("Número de referencias: "+str(numeroReferencias)+" referencia(s)")
    
    
    numeroAutores=len(documento["autores"])
    
    print("Número de autores: "+str(numeroAutores)+" autor(es)")
    
    numeroSecciones=len(documento["contenido"])
    print("Número de secciones: "+str(numeroSecciones)+" seccion(es)")
    
    titulo=documento["titulo"]
    
    tokens=nltk.word_tokenize(titulo)
    
    
    tamanioTitulo=len(tokens)
    
    
    abs_titulo=""
    text=""
    print("Tamaño del titulo: "+str(tamanioTitulo)+" palabra(s)")
    
    for cont in documento["abstract"]:
        #print(cont["header"])
        abs_titulo=cont["header"]
        
        for t in cont["text"]:
            text=t
            
    abstract=" ".join([abs_titulo,t])
    
    abstract_tokens=len(nltk.wordpunct_tokenize(abstract))
    
    print("Tamaño del abstract: "+str(abstract_tokens)+" palabras")
    #print(abstract)
    completo=""
    for cont in documento["contenido"]:
        
        for t in cont["text"]:
            completo+=t
            
    sentCont=nltk.sent_tokenize(completo)
    wCont=nltk.word_tokenize(completo)
    
    print("Numero de oraciones:"+str(len(sentCont))+" oraciones")
    
    print("El texto tiene: "+str(len(wCont))+" palabras en total")
            