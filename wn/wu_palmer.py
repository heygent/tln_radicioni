import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
from nltk.corpus.reader import wup_similarity
import csv


def lcs(sense_1: Synset, sense_2: Synset) -> Synset:

    # calcola tutti i percorsi degli iperonimi
    hypernym_paths1 = sense_1.hypernym_paths()
    hypernym_paths2 = sense_2.hypernym_paths()

    # creo due insiemi contenenti tutti gli iperonimi
    all_hypernims1 = {synset for synsets in hypernym_paths1 for synset in synsets}
    all_hypernims2 = {synset for synsets in hypernym_paths2 for synset in synsets}

    # calcolo l'intersezionetra i  due insiemi di iperonimi, ovvero l'insieme degli antenati comuni
    intersection = all_hypernims1.intersection(all_hypernims2)

    # tra gli antenati comuni prendo quello il cui percorso minimo alla radice è più lungo degli altri antenati
    if intersection:
        LCS: Synset = max(intersection, key=lambda x: x.min_depth())
    else:
        LCS = None

    return LCS


def wu_palmer(sense_1: Synset, sense_2: Synset):

    LCS = lcs(sense_1, sense_2)

    if not LCS:
        return 0

    LCS_depth = LCS.max_depth() + 1

    s1_lcs_distance = sense_1.shortest_path_distance(LCS)
    s2_lcs_distance = sense_2.shortest_path_distance(LCS)

    s1_depth = s1_lcs_distance + LCS_depth
    s2_depth = s2_lcs_distance + LCS_depth

    return (2.0 * LCS_depth) / (s1_depth + s2_depth)


def my_wup_similarity():
    nltk.download('wordnet')

    # print(wup_similarity(wn.synsets("Book")[0], wn.synsets("Football")[0]))
    with open('resources/WordSim353.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []

        for row in reader:
            synsets_1 = wn.synsets(row["word_1"])
            synsets_2 = wn.synsets(row["word_2"])

            max_similarity = max(wu_palmer(sense_1, sense_2)
                            for sense_1 in synsets_1
                            for sense_2 in synsets_2
                            )

            result.append(max_similarity)

        return result

if __name__ == "__main__":
    my_wup_similarity()