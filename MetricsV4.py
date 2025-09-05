import nltk
import re
from lexicalrichness import LexicalRichness
from npl_models import nlp #Natural Language Processing models
from readability import Readability

#print(cupy.show_config())

"""
Esta es la última versión del script de las metricas.

El principal cambio es que la función cleanText esta encamida al uso de los modelo Expei 

la Carga de spacy no la hice aquí por cuestiones de despliegue en en servidor pero bastaría con poner

 spacy.require_cpu()
 npl=spacy.load("en_core_web_sm",disable=["parser", "ner"]) #Hay que descargar el modelo de ingles de spacy
"""

#print(npl.pipe_names)


#nltk.download('stopwords')

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
    return texto


def wordsTagged(texto):#*Funcion para etiquetar las palabras y solo permitir las que tienen un valor lexico
    #python -m spacy download en_core_web_sm
    doc=nlp(texto)
    #for token in doc: #Este ciclo se creo para analizar como son etiquedas las palbras antes de filtrarlas por su peso lexico
        #print(f"{token.text}-->{token.pos_}")
    tagged=[token.text.lower() for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]]
    return set(tagged)
def getFunctionWords(texto):#Función para obtener las function words
  
  info=nlp(texto)
  functionwords=[token.text.lower() for token in info if token.is_stop]
  setfunctionwords=set(functionwords)
  return setfunctionwords


def tokenizeWords(texto):#Separador de palabras
    listPalabras=nltk.word_tokenize(texto)
    #Split the words from the not alphabetic characters
    listPalabrasValidadas=[token for token in listPalabras if token.isalpha()]
    #print("Numero de palabras: ",len(listPalabrasValidadas))
    return listPalabrasValidadas


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

def getEasyWords():#Función para obtener las 3000 palabras más faciles del idioma inglés
    #path = os.path.join(os.path.dirname(__file__),"txts", "3000easyWords.txt")
    path="./txts/3000easyWords.txt"
    with open(path,encoding="utf-8") as f:
        return tokenizeWords(f.read())

#////////////////////////////////////////////////////////////////////////////////////////////////////
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
    textTokenized=tokenizeWords(texto)
    functionWords=getFunctionWords(texto)
    listEasyWords=getEasyWords()
    listLexWords=[w for w in textTokenized if((w.lower()not in functionWords) and w.isalpha()==True)]
    print("Unidades lexicas",listLexWords)

    listHardWords=[w.lower() for w in textTokenized if(((w.lower() not in listEasyWords) and (w.lower() in listLexWords)) and (len(w)>3))]
    print("Palabras sofisticadas: ",len(listHardWords))

    sofisticidad=len(listHardWords)/float(listLexWords)
    return sofisticidad

def calculateTaggedLexicalDensity(texto):
    tokenized=tokenizeWords(texto)
    tagged=wordsTagged(texto)
    print("Palabras etiquetadas: ",len(tagged))
    print("Palabras totales: ",len(tokenized))
    uniqueTagged=set(tagged)
    print("Palabras etiquetadas únicas: ",uniqueTagged)
    DL_tagged=len(uniqueTagged)/float(len(tokenized))
    return DL_tagged


def calculateTTR(texto):
   
    lex=LexicalRichness(texto)
    return lex.ttr


def calculateTTRRoot(texto):
    lex=LexicalRichness(texto)
    return lex.rttr

def calculateTTRCorrected(texto):
    lex=LexicalRichness(texto)
    return lex.cttr
  
#//////////////////////////////////////////////////////////////////////////////////////////////////////
#*Redeability metrics
def TFRE(texto):
    r = Readability(texto)
    return r.flesch().score

def TFREK(texto):
    r = Readability(texto)
    return r.flesch_kincaid().score

def FogIndex(texto):
    r = Readability(texto)
    return r.gunning_fog().score

def SMOG(texto):
    r = Readability(texto)
    return r.smog().score
#/////////////////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





















