import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
import csv


def find_max_depth():
    return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())


def find_commons_subsumers(sense_1: Synset, sense_2: Synset):
    # calcola tutti i percorsi degli iperonimi
    hypernym_paths1 = sense_1.hypernym_paths()
    hypernym_paths2 = sense_2.hypernym_paths()

    # creo due insiemi contenenti tutti gli iperonimi
    all_hypernims1 = {synset for synsets in hypernym_paths1 for synset in synsets}
    all_hypernims2 = {synset for synsets in hypernym_paths2 for synset in synsets}

    # calcolo l'intersezionetra i  due insiemi di iperonimi, ovvero l'insieme degli antenati comuni
    return all_hypernims1.intersection(all_hypernims2)


def find_minimum_distance(sense: Synset, common_subsumer):
    hypernym_paths = sense.hypernym_paths()

    min = float("inf")

    for path in hypernym_paths:
        if common_subsumer in path:
            reversed_path = list(reversed(path))
            distance = reversed_path.index(common_subsumer)
            if distance < min:
                min = distance

    return min


def sim_path(sense_1, sense_2):

    depthMAX = 20

    commons_subsumers = find_commons_subsumers(sense_1, sense_2)

    if not commons_subsumers:
        return 0

    shortest_path = min(
        find_minimum_distance(sense_1, common_subsumer) +
        find_minimum_distance(sense_2, common_subsumer)
        for common_subsumer in commons_subsumers
    )

    return 2 * depthMAX - shortest_path


def my_sim_path():
    with open('resources/WordSim353.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []

        for row in reader:
            synsets_1 = wn.synsets(row["word_1"])
            synsets_2 = wn.synsets(row["word_2"])

            max_similarity = max(sim_path(sense_1, sense_2)
                            for sense_1 in synsets_1
                            for sense_2 in synsets_2
                            )

            result.append(max_similarity)

        return result


if __name__ == "__main__":
   my_sim_path()