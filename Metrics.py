import spacy
import nltk
import numpy as np
import math
import syllapy
import ast
from npl_models import npl #Natural Language Processing models

def wordsTagged(texto):#*Funcion para etiquetar las palabras y solo permitir las que tienen un valor lexico
    
    
    #python -m spacy download en_core_web_sm
    doc=npl(texto)
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

def getFunctionWords(texto):#Función para obtener las function words
  
  info=npl(texto)
  functionwords=[token.text.lower() for token in info if token.is_stop]
  setfunctionwords=set(functionwords)
  return setfunctionwords

def tokenizeWords(texto):#Separador de palabras
    listPalabras=nltk.word_tokenize(texto)
    #Split the words from the not alphabetic characters
    listPalabrasValidadas=[token for token in listPalabras if token.isalpha()]
    return listPalabrasValidadas

def countSyllables(word):#* Contador de silabas
    return syllapy.count(word)


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
    
def averagetSenteceLengh_perWord(texto):#* Longitud promedio de las oraciones por palabra
    tokenized=tokenizeWords(texto)
    oraciones=splitSentences(texto)
    promedio=len(tokenized)/len(oraciones)
    return(round(promedio,2))


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


def averageSyllabes_perWord(texto):#* Promedio de silabas por palabras
    sumatoriaSilabas=0
    tokenized=tokenizeWords(texto)
    for palabra in tokenized:
        sumatoriaSilabas+=countSyllables(palabra)
    #print(sumatoriaSilabas)
    promedioSilabas=sumatoriaSilabas/len(tokenized)

    return(round(promedioSilabas,2))

def averageWordLength(texto):#* Longitud promedio de las palabras
    words_lenghts=[]
    list_tokenized=tokenizeWords(texto)
    for word in list_tokenized:
        words_lenghts.append(len(word))
    
    aux_array=np.array(words_lenghts)#Creación de un array de numpy para optimizar los calculos
    average_lenght=np.mean(aux_array)

    return average_lenght

#Función para sacar la desviación estandar de las logitudes de las palabras
def std_desviation_of_words_lenghts(texto):
    words_lenghts=[]
    list_tokenized=tokenizeWords(texto)
    for word in list_tokenized:
        words_lenghts.append(len(word))
    aux_array=np.array(words_lenghts)#Creación de un array de numpy para optimizar los calculos
    std_desviation =np.std(aux_array)
    return std_desviation


#////////////////////////////////////////////////////////////////////////////////////////////////////
def calculateTaggedLexicalDensity(texto):
    tokenized=tokenizeWords(texto)
    tagged=wordsTagged(texto)
    DL_tagged=len(tagged)/float(len(tokenized))
    return DL_tagged

def calculateLexicalDensity(texto):

    list_Tokenized=tokenizeWords(texto)
    functionWords=getFunctionWords(texto)

    listaWords=[w.lower() for w in list_Tokenized if(w.lower() not in functionWords) and w.isalpha()==True]#Identificando unidades lexicas
    #print(listaWords)
    DL=len(listaWords)/(float(len(list_Tokenized)))
    return DL

def calculateSophistication(texto):
    textTokenized=tokenizeWords(texto)
    functionWords=getFunctionWords(texto)
    listEasyWords=getEasyWords()
    lenListLexWords=len([w for w in textTokenized if((w.lower()not in functionWords) and w.isalpha()==True)])
    #print(lenListLexWords)
    listWord=[w.lower() for w in textTokenized if(((w.lower()not in listEasyWords) and (w.isalpha()==True)and(w.lower()not in functionWords)) and (len(w)>3))]
    #print(listWord)

    sofisticidad=len(listWord)/float(lenListLexWords)
    return sofisticidad



def calculateSophisticationByLenght(texto):
    
    list_Tokenized=tokenizeWords(texto)
    functionWords=getFunctionWords(texto)
    
    awl=averageWordLength(texto)
    stdd=std_desviation_of_words_lenghts(texto)
    #print(desviacion)
    lexTokens=[w for w in list_Tokenized if(w.lower() not in functionWords) and (w.isalpha())]
    #print(tokensLexicos)
    
    lexSophisticatedTokens=len([w for w in lexTokens if (len(w)>(awl+stdd))])
    #print(NoTokensLexSofisticados)
    
    try:
        SFLexica=lexSophisticatedTokens/float(len(lexTokens))
    except ZeroDivisionError:
        SFLexica=0
        
    return(SFLexica)

def calculateTTR(texto):
    tokenizeWords=tokenizeWords(texto)
    uniqueWors=set(tokenizeWords)
    TTR=len(uniqueWors)/float(len(tokenizeWords))
    return TTR

def calculateTTRTagged(texto):

    tagged=wordsTagged(texto)
    tokenized=tokenizeWords(texto)
    TTRTagged=len(set(tagged))/len(tokenized)
    return TTRTagged
    
def calculateTTRRoot(texto):
    tagged=wordsTagged(texto)
    tokenized=tokenizeWords(texto)
    TTRTagged=len(set(tagged))/math.sqrt(len(tokenized))
    return TTRTagged

def calculateTTRCorregido(texto):
    tagged=wordsTagged(texto)
    tokenized=tokenizeWords(texto)
    TTRTagged=len(set(tagged))/math.sqrt(len(tokenized)*2)
    return TTRTagged
  

#//////////////////////////////////////////////////////////////////////////////////////////////////

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
#/////////////////////////////////////////////////////////////////////////////////////////////////////
#*Preliminar analysis

def count_references_xml(texto):
    try:
        list_references=ast.literal_eval(texto)
    except(ValueError, SyntaxError):
    
        print("No pude parsear:", texto[:50], "…")
        return 0
    return(len(list_references))

def count_authors(texto):
    list_authors = ast.literal_eval(texto)
    return(len(list_authors))

def abstract_size(texto):
    words=tokenizeWords(texto)
    return(len(words))

def number_references(texto):
    references=texto.strip("\n")
    return(len(references))

def number_authors(texto):
    authors=texto.strip(", ")
    return(len(authors))














