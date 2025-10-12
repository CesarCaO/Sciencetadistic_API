import os
import pickle
from scripts import MetricsV4 as mtrs
import fitz
import numpy as np
import re, time
from nltk import word_tokenize, sent_tokenize

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



text=""
pdfs= "./PDFs/test_papers/Accepted/"

langFile = os.listdir(pdfs)

model_files=[
    r"./predictive_model/2_EXPEI_ICLR_2017_PR.pkl",
    r"./predictive_model/2_EXPEI_ICLR_PR.pkl"
]

for file in model_files:
    print(f"\n Loading model from: {file}")

    with open(file,"rb") as f:
        print("Reading Model")
        data = pickle.load(f)
    
    model = data['model']
    vectorizer = data['vectorizer']
    label_encoder = data['label_encoder']
    vocabulario = data['vocabulario']
    caracteristicas = data['caracteristicas']
    pronombres = ['we', 'our', 'us']

    for pdf in langFile:
        pdf_path=os.path.join(pdfs,pdf)
        doc = fitz.open(pdf_path)
        print("Extracting text")
        for page in doc:
            text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')
        doc.close()

        text = mtrs.removeReferences(text)
        text = mtrs.cleanText(text)

        x_test =[text.lower()]
        print("Vectorizing...")
        X_test = vectorizer.transform(x_test)

        print("Calculating Expei")
        fpT, fnpT, contadorPT, contadorNPT = frases(x_test, pronombres, X_test, vocabulario, caracteristicas)
        peit, _ = PeiNei(contadorPT, fpT, contadorNPT, fnpT, X_test)
        expei_test = expei_func(X_test, peit)

        print("Making prediction...")
        y_pred = model.predict(expei_test)

        print(f"{pdf_path}  prediction: ", y_pred)
