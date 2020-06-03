from typing import List
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
import csv


def lcs(word_1, word_2):
    # prendi l'insieme dei synset
    s1: List[Synset] = wn.synsets(word_1)
    s2: List[Synset] = wn.synsets(word_2)
    # calcola tutti i percorsi degli iperonimi
    h1 = s1[0].hypernym_paths()
    h2 = s2[0].hypernym_paths()
    # prendi il percorso più lungo
    max_h1 = max(h1, key=len)
    max_h2 = max(h2, key=len)
    # restituisci l'intersezione dei due percorsi, ovvero gli antenati comuni
    return list(set(max_h1).intersection(max_h2))


def wu_palmer():

    nltk.download('wordnet')

    with open('resources/WordSim353.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(lcs(row["word_1"], row["word_2"]))



if __name__ == "__main__":
    wu_palmer()