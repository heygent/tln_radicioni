from typing import List
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
import csv


def lcs(word_1, word_2):

    # prendi l'insieme dei synset
    synset1: List[Synset] = wn.synsets(word_1)
    synset2: List[Synset] = wn.synsets(word_2)

    # calcola tutti i percorsi degli iperonimi
    hypernym_paths1 = synset1[0].hypernym_paths()
    hypernym_paths2 = synset2[0].hypernym_paths()

    # tra gli antenati comuni prendo quello il cui percorso minimo alla radice è più lungo degli altri antenati
    # calcolo gli antenati comuni intersecando i percorsi alla radice della prima e della seconda parola
    # ogni parola potrebbe avere più percorsi alla radice, effetuiamo l'intersezione tra tutti i percorsi che otteniamo.
    LCS = max([
        max(set(path1).intersection(path2), key=lambda x: x.min_depth())
        for path1 in hypernym_paths1
        for path2 in hypernym_paths2
    ], key=lambda x: x.min_depth())

    return LCS


def wu_palmer():

    nltk.download('wordnet')

    with open('resources/WordSim353.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(lcs(row["word_1"], row["word_2"]))



if __name__ == "__main__":
    wu_palmer()