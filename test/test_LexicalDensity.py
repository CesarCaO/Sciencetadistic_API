from npl_models import nlp
from TRUNAJOD import surface_proxies
import fitz
import MetricsV3 as mtr

"""
with open("./PDFs/Cost_sensitive_selective_naive_Bayes_cla.pdf", "rb") as file:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texto = ""
    for page in doc:
        texto += page.get_text().encode('utf-8').decode('utf-8', errors='ignore')
"""
#texto="Machine learning community is not only interested in maximizing classification accuracy, but also in minimizing the distances between the actual and the predicted class."
texto="Los estudiantes leen libros interesantes en la biblioteca de su escuela"
spacy_doc=nlp(texto)
print(spacy_doc)
print(type(spacy_doc))#spacy.Doc
print("Densidad léxica: ", surface_proxies.lexical_density(spacy_doc))

"""
#* Método propio
print("Densidad lexica: ", mtr.calculateTaggedLexicalDensity(texto))
"""