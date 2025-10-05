import pandas as pd
import numpy as np
import pickle
import re, time
from nltk import word_tokenize, sent_tokenize
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix


"""
pdfs = "./PDFs/test_papers/"
langFile = os.listdir(pdfs)
text=""
"""
#*Open the two datasets with PeerRead (df1) and ASAP (df2)
path_1="./CSVs/INCOMPLETO_BOW_Completo.csv"
path_2="./CSVs/Particiones_COMPLETO.csv"

path_full = "./CSVs/CSVsUnidos.csv"
print("Leyendo Datasets")
#df1=pd.read_csv(path_1, encoding="utf-8")
#df2=pd.read_csv(path_2, encoding="utf-8")

dfFull = pd.read_csv(path_full, encoding="utf-8")

#print("Dataset 1",df1.columns)
#print(df1["Conferencia"].unique())

#print("Dataset 2",df2.columns)
#print(df2["Conferencia"].unique())

print("Dataset 3",dfFull.columns)
print(dfFull["Conferencia"].unique())

# === Funciones auxiliares ===
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

"""

# === Cargar modelo entrenado Peer Read ===
with open(R"./predictive_model/2_EXPEI_PEER_READ.pkl","rb") as file1:
    data = pickle.load(file1)

    model = data['model']
    vectorizer = data['vectorizer']
    label_encoder = data['label_encoder']
    vocabulario = data['vocabulario']
    caracteristicas = data['caracteristicas']
    pronombres = ['we', 'our', 'us']

    #Loading df1 data
    print("Loading testing data")
    test_df1=df1[df1["Particion"]=="test"].reset_index(drop=True)

    x_test = test_df1['Texto Completo'].str.lower().apply(str).values
    y_test = test_df1['Accepted']
    y_te = label_encoder.transform(y_test)

    X_test = vectorizer.transform(x_test)

    # === Calcular EXPEI ===
    fpT, fnpT, contadorPT, contadorNPT = frases(x_test, pronombres, X_test, vocabulario, caracteristicas)
    peit, _ = PeiNei(contadorPT, fpT, contadorNPT, fnpT, X_test)
    expei_test = expei_func(X_test, peit)

    # === Evaluación ===
    y_pred = model.predict(expei_test)

    print("\n--- RESULTADOS EN TEST ---")
    print(classification_report(y_te, y_pred, digits=3))
    print("Matriz de confusión:")
    print(confusion_matrix(y_te, y_pred))
    print(f"Accuracy: {accuracy_score(y_te, y_pred) * 100:.4f}%")
    print(f"Macro F1: {f1_score(y_te, y_pred, average='macro') * 100:.4f}%")
"""

"""
#*Cargar modelo entrenado ASAP

with open(R"./predictive_model/2_EXPEI_ASAP.pkl","rb") as file2:
    data = pickle.load(file2)

    model = data['model']
    vectorizer = data['vectorizer']
    label_encoder = data['label_encoder']
    vocabulario = data['vocabulario']
    caracteristicas = data['caracteristicas']
    pronombres = ['we', 'our', 'us']

    #Loading df2 data
    print("Loading testing data")
    test_df2=df2[df2["Particion"]=="test"].reset_index(drop=True)

    x_test = test_df2['Texto Completo'].str.lower().apply(str).values
    y_test = test_df2['Accepted']
    y_te = label_encoder.transform(y_test)

    X_test = vectorizer.transform(x_test)

     # === Calcular EXPEI ===
    print("Calculating Expei")
    fpT, fnpT, contadorPT, contadorNPT = frases(x_test, pronombres, X_test, vocabulario, caracteristicas)
    peit, _ = PeiNei(contadorPT, fpT, contadorNPT, fnpT, X_test)
    expei_test = expei_func(X_test, peit)

    print("Evaluating")

    # === Evaluación ===
    y_pred = model.predict(expei_test)

    print("\n--- RESULTADOS EN TEST ---")
    print(classification_report(y_te, y_pred, digits=3))
    print("Matriz de confusión:")
    print(confusion_matrix(y_te, y_pred))
    print(f"Accuracy: {accuracy_score(y_te, y_pred) * 100:.4f}%")
    print(f"Macro F1: {f1_score(y_te, y_pred, average='macro') * 100:.4f}%")
"""



with open(R"./predictive_model/2_EXPEI_PEER_READ.pkl","rb") as file3:
    print("Cargando Pickle")
    data = pickle.load(file3)

    print("Configurando modelo")
    model = data['model']
    vectorizer = data['vectorizer']
    label_encoder = data['label_encoder']
    vocabulario = data['vocabulario']
    caracteristicas = data['caracteristicas']
    pronombres = ['we', 'our', 'us']

    #Loading df2 data
    print("Obteniendo datos de testeo del CSV")
    print("Loading testing data")
    test_dfFull=dfFull[dfFull["Particion"]=="test"].reset_index(drop=True)
    print("La cantidad de datos de testeo son: ",len(test_dfFull))

    print("Obteniendo textos")
    x_test = test_dfFull['Texto Completo'].str.lower().apply(str).values
    print("Obteniendo textos aceptados")
    y_test = test_dfFull['Accepted']
    print("Aplicando transformadores")
    y_te = label_encoder.transform(y_test)

    X_test = vectorizer.transform(x_test)

     # === Calcular EXPEI ===
    print("Calculating Expei")
    fpT, fnpT, contadorPT, contadorNPT = frases(x_test, pronombres, X_test, vocabulario, caracteristicas)
    peit, _ = PeiNei(contadorPT, fpT, contadorNPT, fnpT, X_test)
    expei_test = expei_func(X_test, peit)

    print("Evaluating")

    # === Evaluación ===
    y_pred = model.predict(expei_test)

    print("\n--- RESULTADOS EN TEST ---")
    print(classification_report(y_te, y_pred, digits=3))
    print("Matriz de confusión:")
    print(confusion_matrix(y_te, y_pred))
    print(f"Accuracy: {accuracy_score(y_te, y_pred) * 100:.4f}%")
    print(f"Macro F1: {f1_score(y_te, y_pred, average='macro') * 100:.4f}%")




  


    
    
    
    
