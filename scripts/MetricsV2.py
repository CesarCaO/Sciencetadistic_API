import spacy
import nltk
import numpy as np
import math
import syllapy
import ast
import re
from lexicalrichness import LexicalRichness
from config.nlp_models import npl #Natural Language Processing models

#print(cupy.show_config())



#print(npl.pipe_names)


#nltk.download('stopwords')
"""
def spacy_funcion_words():
    stopwords= npl.Defaults.stop_words
    listStopwords=[w for w in stopwords]
    return listStopwords
"""
#Función creada por Gamaliel
def cleanText(texto):
    # Elimina líneas que contienen solo un número entre saltos de línea, por ejemplo: '\n12\n'
    texto = re.sub(r'\n\d+\n', '\n', texto)
    # Elimina números que aparecen como palabras completas (por ejemplo: "en 2023 el estudio..." → "en el estudio...")
    texto = re.sub(r'\b\d+\b', '', texto)
    # Elimina cualquier secuencia de dígitos, estén donde estén (por ejemplo: "abc123def" → "abcdef")
    texto = re.sub(r'\d+', '', texto)
    # Reemplaza múltiples saltos de línea por un solo espacio, y elimina espacios al principio y final
    texto = re.sub(r'\n+', ' ', texto).strip()
    # Elimina cualquier salto de línea restante
    texto = texto.replace('\n', '')
     # Eliminar caracteres que no sean comas, puntos y puntos y comar. Acepta acentos y la letra ñ
    texto = re.sub(r"[^\w\s.,;áéíóúÁÉÍÓÚñÑ]", "", texto)
    #Elimina cualquier coma/punto/punto y coma que esté aislado entre espacios
    texto = re.sub(r'(?<=\s)[.,;]+(?=\s)', '', texto)
    #Colapsa múltiples espacios en uno solo
    texto = re.sub(r'\s{2,}', ' ', texto).strip()

    #Eliminar repeticiones innecesarias
    texto = re.sub(r'([.,;])(?:\s*\1)+', r'\1', texto) 
    return texto


"""
def wordsTagged(texto):#*Funcion para etiquetar las palabras y solo permitir las que tienen un valor lexico
    
    #python -m spacy download en_core_web_sm
    doc=npl(texto)
    #for token in doc: #Este ciclo se creo para analizar como son etiquedas las palbras antes de filtrarlas por su peso lexico
        #print(f"{token.text}-->{token.pos_}")
    tagged=[token.text.lower() for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]]

    return set(tagged)

def splitSentences(texto):#Funcion para separar las oraciones
    sentences=nltk.sent_tokenize(texto)
    return sentences

def getEasyWords():#Función para obtener las 3000 palabras más faciles del idioma inglés
    
    #path = os.path.join(os.path.dirname(__file__),"txts", "3000easyWords.txt")
    path="./txts/3000easyWords.txt"
    with open(path,encoding="utf-8") as f:
        return tokenizeWords(f.read())
"""

def getFunctionWords(texto):#Función para obtener las function words
  
  info=npl(texto)
  functionwords=[token.text.lower() for token in info if token.is_stop]
  setfunctionwords=set(functionwords)
  return setfunctionwords


def tokenizeWords(texto):#Separador de palabras
    listPalabras=nltk.word_tokenize(texto)
    #Split the words from the not alphabetic characters
    listPalabrasValidadas=[token for token in listPalabras if token.isalpha()]
    #print("Numero de palabras: ",len(listPalabrasValidadas))
    return listPalabrasValidadas

"""
def countSyllables(word):#* Contador de silabas
    return syllapy.count(word)
"""
"""
def count_multisyllables_per_100_words(texto):#* Contar número de palabras multisilabicas en 100 palabras
    list_2SyllablesWords=[]
    tokenized=tokenizeWords(texto)
    current_group=[]

    for palabra in tokenized:
        current_group.append(palabra)

        if len(current_group)==100:
            for word_grupo in current_group:
                if countSyllables(word_grupo)>2:
                    list_2SyllablesWords.append(word_grupo)
            current_group=[]
    return list_2SyllablesWords
"""
""" 
def averagetSenteceLengh_perWord(texto):#* Longitud promedio de las oraciones por palabra
    tokenized=tokenizeWords(texto)
    oraciones=splitSentences(texto)
    promedio=len(tokenized)/len(oraciones)
    return(round(promedio,2))
"""
"""

def count_multisyllables_per_30_sentences(texto):#* Palabras multisilabicas en 30 oraciones
    list_2SyllablesWords=[]
    current_group=[]
    sentences = splitSentences(texto)
    for sentence in sentences:
        current_group.append((sentence))
        if(len(current_group))==30:

            for sentence_group in current_group:

                sentence_word=tokenizeWords(sentence_group)

                for word in sentence_word:

                    if(countSyllables(word)>2):

                        list_2SyllablesWords.append(word)
            current_group=[]
    return(len(list_2SyllablesWords))
"""
"""

def averageSyllabes_perWord(texto):#* Promedio de silabas por palabras
    sumatoriaSilabas=0
    tokenized=tokenizeWords(texto)
    for palabra in tokenized:
        sumatoriaSilabas+=countSyllables(palabra)
    #print(sumatoriaSilabas)
    promedioSilabas=sumatoriaSilabas/len(tokenized)

    return(round(promedioSilabas,2))
"""
"""
def averageWordLength(texto):#* Longitud promedio de las palabras
    words_lenghts=[]
    list_tokenized=tokenizeWords(texto)
    for word in list_tokenized:
        words_lenghts.append(len(word))
    
    aux_array=np.array(words_lenghts)#Creación de un array de numpy para optimizar los calculos
    average_lenght=np.mean(aux_array)

    return average_lenght
"""
"""
#Función para sacar la desviación estandar de las logitudes de las palabras
def std_desviation_of_words_lenghts(texto):
    words_lenghts=[]
    list_tokenized=tokenizeWords(texto)
    for word in list_tokenized:
        words_lenghts.append(len(word))
    aux_array=np.array(words_lenghts)#Creación de un array de numpy para optimizar los calculos
    std_desviation =np.std(aux_array)
    return std_desviation
"""
def removeReferences(texto):
    #multilanguage regex to remove references
    textoLower=texto.lower()
    headers={
        r'references',
        r'referencias',
        r'bibliography',
        r'bibliografía',
        r'citas',
        r'citations',
        r'works cited',
    }

    header_patern=r'(?mi)^[ \t]*(?:' + '|'.join(headers) + r')[ \t]*$'

    match=re.search(header_patern,textoLower)
    if match:
        return textoLower[:match.start()]
    else:
        return textoLower

#////////////////////////////////////////////////////////////////////////////////////////////////////
"""
def calculateTaggedLexicalDensity(texto):
    tokenized=tokenizeWords(texto)
    tagged=wordsTagged(texto)
    print("Palabras etiquetadas: ",len(tagged))
    print("Palabras totales: ",len(tokenized))
    uniqueTagged=set(tagged)
    print("Palabras etiquetadas únicas: ",uniqueTagged)
    DL_tagged=len(uniqueTagged)/float(len(tokenized))
    return DL_tagged
"""
def calculateLexicalDensity(texto):

    list_Tokenized=tokenizeWords(texto)
    functionWords=getFunctionWords(texto)

    #print("Funcion words: ",functionWords)

    listWords=[w.lower() for w in list_Tokenized if(w.lower() not in functionWords) and w.isalpha()==True]#Identificando unidades lexicas
    #print("Unidades léxicas: ",listWords)	
    #print("Palabras totales: ",len(list_Tokenized))

    uniqueWords=set(listWords)
    #print("Palabras léxicas únicas: ",uniqueWords)


    DL=len(uniqueWords)/(float(len(list_Tokenized)))# Es necesario float para evitar una division entera
    return DL
"""
def calculateSophistication(texto):
    textTokenized=tokenizeWords(texto)#Separar el texto por tokens
    functionWords=getFunctionWords(texto)#Obtener las stopwords del texto
    listEasyWords=getEasyWords()#Obtener las lista de palabras fáciles del idióma inglés
    listLexWords=[w for w in textTokenized if((w.lower()not in functionWords) and w.isalpha()==True)]#Identificar las unidades léxicas del texto
    print("Unidades lexicas",set(listLexWords))
    print("Número de unidades léxicas: ",len(listLexWords))

    listHardWords=[w.lower() for w in listLexWords if(((w.lower() not in listEasyWords) and (len(w)>3)))]#De las unidades léxicas, identificar las palabras dificiles o sofisticadas y cuya longitud sea mayor a 3 letras
    print("Palabras sofisticadas: ",set(listHardWords))
    print("Número de palabras sofisticadas: ",len(listHardWords))

    sofisticidad=len(set(listHardWords))/float(len(set(listLexWords)))
    return sofisticidad
"""

"""
def calculateSophisticationByLength(texto):
    
    list_Tokenized=tokenizeWords(texto)#*Separar el texto por palabras
    functionWords=getFunctionWords(texto)#*Obtener las stopwords del texto
    awl=averageWordLength(texto)#*Obtener el promedio de la longitud de las palabras
    stdd=std_desviation_of_words_lenghts(texto)#*Obtener la desviación estandar del promedio de longitud de las palabras
    lexTokens=[w for w in list_Tokenized if(w.lower() not in functionWords) and (w.isalpha())]#*Obtener los tokens lexicos
    lexSophisticatedTokens=len([w for w in lexTokens if (len(w)>(awl+stdd))])#*Obtener los tokens lexicos sofisticados basandose en la lognitud

    print("Promedio de longitud de palabras: ", awl)
    print("Desviación estandar de longitud de palabras: ", stdd)
    print("Palabras lexicas: ",lexTokens)
    print("Palabras sofisticadas: ", lexSophisticatedTokens)
    try:
        SFLexica=lexSophisticatedTokens/float(len(lexTokens))
    except ZeroDivisionError:
        SFLexica=0
        
    return(SFLexica)
"""
def calculateTTR(texto):
    """
    uniqueWors=set(words)
    TTR=len(uniqueWors)/float(len(words))
    return TTR
    """
    lex=LexicalRichness(texto)
    return lex.ttr

"""
def calculateTTRTagged(texto):

    tagged=wordsTagged(texto)
    tokenized=tokenizeWords(texto)
    TTRTagged=len(set(tagged))/len(tokenized)
    return TTRTagged
"""  

def calculateTTRRoot(texto):
    tokenized=tokenizeWords(texto)
    TTRTagged=len(set(tokenized))/math.sqrt(len(tokenized))
    return TTRTagged

def calculateTTRCorregido(texto):
    tokenized=tokenizeWords(texto)
    TTRTagged=len(set(tokenized))/math.sqrt((2*len(tokenized)))
    return TTRTagged
  

#//////////////////////////////////////////////////////////////////////////////////////////////////
"""
#*Readability metrics

#*The Flesch Reading Ease score

def TFRE(texto):
    score=206.835-(1.015 * averagetSenteceLengh_perWord(texto))-(84.6 * averageSyllabes_perWord(texto))
    return score

#*The Flesch-Kincaid readability formula
def The_Flesch_Kincaid(texto):
    gl=(0.4 * averagetSenteceLengh_perWord(texto)) + (12 * averageSyllabes_perWord(texto)) - 15
    return gl

#*The Fog Index
#* GL = 0.4 * (average sentence lenght + hard words)
def The_Fog_Index(texto):
    gl=0.4*(averagetSenteceLengh_perWord(texto)+len(count_multisyllables_per_100_words(texto)))
    return gl

#The SMOG Index

def The_SMOG_Index(texto):
    smog=3+math.sqrt(count_multisyllables_per_30_sentences(texto))
    return smog
"""
#/////////////////////////////////////////////////////////////////////////////////////////////////////
"""
#*Preliminar analysis

def count_references(texto):
    texto=texto.strip().strip('"').strip("'")
    try:
        list_references=ast.literal_eval(texto)
    except(ValueError, SyntaxError):
    
        print("No pude parsear:", texto[:50], "…")
        return 0
    return(len(list_references))

#def count_authors(texto):
    #list_authors = ast.literal_eval(texto)
    #return(len(list_authors))
"""
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////






















