import nltk
import re
import re, time
from nltk import word_tokenize, sent_tokenize
import numpy as np
from lexicalrichness import LexicalRichness
from config.nlp_models import nlp#Natural Language Processing models
from config.EasyFunctionWord import STOP_WORDS,EASY_WORDS
from readability import Readability
from config.startup_EXPEI import model,vectorizer,label_encoder,vocabulario,caracteristicas,pronombres


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
    return [token for token in listPalabras if token.isalpha()]


def removeReferences(texto):
    #multilanguage regex to remove references
    #textoLower=texto.lower()
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

    match=re.search(header_patern,texto)
    if match:
        return texto[:match.start()]
    else:
        return texto

#def getEasyWords():#Función para obtener las 3000 palabras más faciles del idioma inglés
    #path = os.path.join(os.path.dirname(__file__),"txts", "3000easyWords.txt")
    #path="./data/3000easyWords.txt"
    #with open(path,encoding="utf-8") as f:
        #easyWords = tokenizeWords(f.read())
        #f.close()
        #return easyWords

#* Funciones auxiliares 
def frases(pdfs, pronombres, x, vocabulario, caracteristicas):
    start_time = time.time()
    m, n = x.shape
    fp = np.zeros((m, n))
    fnp = np.zeros((m, n))
    contadorP = []
    contadorNP = []

    for i in range(len(pdfs)):
        texto = pdfs[i]
        countP = 0
        countNP = 0
        for por_oracion in sent_tokenize(texto):
            lista = re.split("(?:\n|\r|\r\n?)+", por_oracion)
            for oracion in lista:
                if not re.search(r"^\s*$", oracion):
                    LiTokPronom = word_tokenize(oracion)
                    inter = len(set(pronombres) & set(LiTokPronom))
                    if inter > 0:
                        countP += 1
                        for palabra in set(LiTokPronom) & set(caracteristicas):
                            fp[i][vocabulario[palabra]] += 1
                    else:
                        countNP += 1
                        for palabra in set(LiTokPronom) & set(caracteristicas):
                            fnp[i][vocabulario[palabra]] += 1

        contadorP.append(countP)
        contadorNP.append(countNP)

    print(f"Tiempo de ejecución para 'frases': {time.time() - start_time:.2f} segundos.")
    return fp, fnp, contadorP, contadorNP

def PeiNei(contadorP, fp, contadorNP, fnp, x_):
    start_time = time.time()
    m, n = x_.shape
    pei = np.zeros((m, n))
    nei = np.zeros((m, n))

    for i in range(m):
        for j in range(n):
            if contadorP[i] > 0 and fp[i][j] > 0:
                p = fp[i][j] / (fp[i][j] + fnp[i][j])
                r = fp[i][j] / contadorP[i]
                if (p + r) != 0:
                    pei[i][j] = 2 * (p * r) / (p + r)
            if contadorNP[i] > 0 and fnp[i][j] > 0:
                p = fnp[i][j] / (fp[i][j] + fnp[i][j])
                r = fnp[i][j] / contadorNP[i]
                if (p + r) != 0:
                    nei[i][j] = 2 * (p * r) / (p + r)

    print(f"Tiempo de ejecución para 'PeiNei': {time.time() - start_time:.2f} segundos.")
    return pei, nei

def expei_func(x_, pei):
    start_time = time.time()
    m, n = x_.shape
    tf = x_.toarray()
    expei_val = np.zeros((m, n))

    for f in range(m):
        for c in range(n):
            if tf[f][c] > 0:
                expei_val[f][c] = pow(np.sqrt(tf[f][c]), float(1.0 - pei[f][c]))

    print(f"Tiempo de ejecución para 'expei_func': {time.time() - start_time:.2f} segundos.")
    return expei_val

#////////////////////////////////////////////////////////////////////////////////////////////////////


def calculateSophistication(texto):
    tokens=tokenizeWords(texto)
    
    tokens_lower = [w.lower() for w in tokens]
    tokens_lower_set = set(tokens_lower)
   
    lex_Words= [w for w in tokens_lower if w not in STOP_WORDS]
    

    if not lex_Words:  # Evitar división por cero
        return 0.0
    
    hard_words_count = sum(
        1 for w in lex_Words 
        if w not in EASY_WORDS and len(w) > 3
    )
    sophistication = hard_words_count / len(lex_Words)
    return sophistication

def calculateLexicalDensity(texto):
    
    if not texto or not texto.strip():
        return 0.0
    
    tokenized=tokenizeWords(texto)
    tokens_lower = [w.lower() for w in tokenized]
    #tagged=wordsTagged(texto)
    lex_Words= [w for w in tokens_lower if w not in STOP_WORDS]
    if not lex_Words:  # Evitar división por cero
        return 0.0
    
    #print("Palabras etiquetadas: ",len(tagged))
    #print("Palabras totales: ",len(tokenized))
    #uniqueTagged=set(tagged)
    #print("Palabras etiquetadas únicas: ",uniqueTagged)
    DL_tagged=len(lex_Words)/float(len(tokenized))
    return DL_tagged


def calculateTTR(texto):
   
    lex=LexicalRichness(texto)
    return (lex.ttr)


def calculateTTRRoot(texto):
    lex=LexicalRichness(texto)
    return (lex.rttr)

def calculateTTRCorrected(texto):
    lex=LexicalRichness(texto)
    return (lex.cttr)
  
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
def prediction (texto):
    x_test = [texto.lower()]
    X_test = vectorizer.transform(x_test)

    fpT, fnpT, contadorPT, contadorNPT = frases(x_test, pronombres, X_test, vocabulario, caracteristicas)
    peit, _ = PeiNei(contadorPT, fpT, contadorNPT, fnpT, X_test)
    expei_test = expei_func(X_test, peit)

    return model.predict(expei_test)
    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





















