import nltk
import spacy

nltk.download('punkt', quiet=True)
spacy.cli.download("en_core_web_sm")
spacy.require_cpu()
npl = spacy.load("en_core_web_sm", disable=["parser", "ner"])