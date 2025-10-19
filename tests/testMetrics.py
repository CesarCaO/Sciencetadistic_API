from scripts import MetricsV4
import fitz

file= "./PDFs/test_papers/Accepted/Cost_sensitive_selective_naive_Bayes_cla.pdf"

doc = fitz.open(file, filetype="pdf")
text = ""
for page in doc:
    text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

text= MetricsV4.removeReferences(text)
text= MetricsV4.cleanTextForMetrics(text)

#text= "the dog eats dog food"
print(MetricsV4.calculateLexicalDensity(text))