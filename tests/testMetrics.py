from scripts import MetricsV4
import fitz

file= "./PDFs/Cost_sensitive_selective_naive_Bayes_cla.pdf"

doc = fitz.open(file, filetype="pdf")
text = ""
for page in doc:
    text+=page.get_text().encode('utf-8').decode('utf-8',errors='ignore')

print(MetricsV4.calculateLexicalDensity(text))