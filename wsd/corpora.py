"""
Scarica i corpora necessari all'esecuzione del programma tramite NLTK.
"""
import nltk

CORPORA = ['wordnet', 'semcor']


def download_corpora():
    for corpus in CORPORA:
        nltk.download(corpus, raise_on_error=True)


if __name__ == '__main__':
    download_corpora()
