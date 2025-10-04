import nltk
import spacy

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
spacy.cli.download("en_core_web_sm")
#spacy.cli.download("es_core_news_sm")

# Configuración CORRECTA del modelo
spacy.require_cpu()  # Primero requerir CPU
nlp = spacy.load(  # Luego cargar el modelo
    "en_core_web_sm", 
    disable=["ner", "textcat", "parser", "lemmatizer"]  # Deshabilitar más componentes para eficiencia
)

