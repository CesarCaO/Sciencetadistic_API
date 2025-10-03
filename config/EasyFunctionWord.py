import nltk
from config.nlp_models import nlp#Natural Language Processing models

_EASY_WORDS_CACHE = None

def load_easy_words():
    global _EASY_WORDS_CACHE
    if _EASY_WORDS_CACHE is None:
        path = "./data/3000easyWords.txt"
        with open(path, encoding="utf-8") as f:
            words = nltk.word_tokenize(f.read())
        _EASY_WORDS_CACHE = frozenset(w.lower() for w in words if w.isalpha())
    return _EASY_WORDS_CACHE

EASY_WORDS = load_easy_words()

STOP_WORDS = nlp.Defaults.stop_words