from typing import List
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
from nltk.corpus.reader import wup_similarity
import csv


def lcs(synset1: Synset, synset2: Synset) -> Synset:

    # calcola tutti i percorsi degli iperonimi
    hypernym_paths1 = synset1.hypernym_paths()
    hypernym_paths2 = synset2.hypernym_paths()

    # creo due liste contenenti tutti gli iperonimi
    all_hypernims1 = {synset for synsets in hypernym_paths1 for synset in synsets}
    all_hypernims2 = {synset for synsets in hypernym_paths2 for synset in synsets}

    # calcolo l'intersezioni delle due liste di iperonimi, ovvero gli antenati comuni
    intersection = all_hypernims1.intersection(all_hypernims2)

    # tra gli antenati comuni prendo quello il cui percorso minimo alla radice è più lungo degli altri antenati
    LCS: Synset = max(intersection, key=lambda x: x.min_depth())

    return LCS


def wu_palmer():

    nltk.download('wordnet')

    # print(wup_similarity(wn.synsets("Book")[0], wn.synsets("Football")[0]))
    with open('resources/WordSim353.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        result = []

        for row in reader:
            synset1: List[Synset] = wn.synsets(row["word_1"])
            synset2: List[Synset] = wn.synsets(row["word_2"])

            LCS = lcs(synset1[0], synset2[0])
            LCS_depth = LCS.max_depth() + 1

            s1_lcs_distance = synset1[0].shortest_path_distance(LCS)
            s2_lcs_distance = synset2[0].shortest_path_distance(LCS)

            s1_depth = s1_lcs_distance + LCS_depth
            s2_depth = s2_lcs_distance + LCS_depth

            result.append(2.0 * LCS_depth / (s1_depth + s2_depth))

        return result

# def wup_similarity():
#     nltk.download('wordnet')
#
#     # print(wup_similarity(wn.synsets("Book")[0], wn.synsets("Football")[0]))
#     with open('resources/WordSim353.csv') as csvfile:
#         reader = csv.DictReader(csvfile)
#         result = []
#         for row in reader:
#
#             temp_result = [
#                 wu_palmer(sense_1, sense_2)
#              ] for sense_1 in wn.synsets(row["word_1"] for sense_2 in wn.synsets(row["word_2"]


if __name__ == "__main__":
    wu_palmer()