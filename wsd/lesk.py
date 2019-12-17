import re
from typing import List, Set
from nltk.corpus.reader import Synset
from nltk.corpus import wordnet as wn


def most_frequent_synset(synsets: List[Synset]) -> Synset:
    """
    Data una lista di synset, restituisce il Synset con la maggior
    occorrenza di lemmi nel corpus.
    :param synsets: Una lista di Synset.
    :return: Il Synset con maggior occorrenza di lemmi nel corpus.
    """
    return max(
        synsets,
        key=lambda synset: sum(lemma.count() for lemma in synset.lemmas())
    )


def synset_to_bag_of_words(synset: Synset) -> Set[str]:
    sources = [synset.definition(), *synset.examples()]
    result = set()

    for sentence in sources:
        result.update(sentence_to_bag_of_words(sentence))

    return result


def sentence_to_bag_of_words(sentence: str) -> Set[str]:
    """
    Data una frase, restituisce un set contenente le sue parole normalizzate.
    La normalizzazione non esegue operazioni di lemmatizzazione, si limita a
    rimuovere la punteggiatura e le lettere maiuscole.
    :param sentence: Una frase
    :return: Un set di parole normalizzate contenute nella frase.
    """
    sentence = sentence.lower()
    bow = set(re.split(r'[^\w\d°]+', sentence))
    bow.discard('')
    return bow


def compute_overlap(bag1: Set[str], bag2: Set[str]) -> int:
    """
    A partire da due set, restituisce il numero di elementi nella loro
    intersezione.
    :param bag1: Un set.
    :param bag2: Un set.
    :return: Il numero di occorrenze nell'intersezione di bag1 e bag2.
    """
    return sum(1 for word in bag1 if word in bag2)


def lesk(sentence: List[str], target_i: int) -> Synset:
    """
    Applica l'algoritmo di Lesk per eseguire la disambiguazione del senso di
    una parola all'interno di una frase.
    :param sentence: Una frase.
    :param target_i: L'indice della parola di cui si vuole disambiguare il
    senso nella frase.
    :return: Il Synset WordNet contente il senso più probabile per quella
    parola.
    """
    target = sentence[target_i]
    word_synsets = wn.synsets(target)
    sentence_bow = set(sentence)

    best_synset = most_frequent_synset(word_synsets)
    max_overlap = 0

    for synset in word_synsets:
        synset_bow = synset_to_bag_of_words(synset)
        overlap = compute_overlap(sentence_bow, synset_bow)

        if overlap > max_overlap:
            max_overlap = overlap
            best_synset = synset

    return best_synset
