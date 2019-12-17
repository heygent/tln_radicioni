from wsd import lesk
from nltk.corpus import wordnet as wn


def test_sentence_to_bag_of_words():
    sentence = "Pigs, we **get** what pigs deserve."
    expected = {'pigs', 'we', 'get', 'what', 'pigs', 'deserve'}

    bag_of_words = lesk.sentence_to_bag_of_words(sentence)

    assert bag_of_words == expected


def test_synset_to_bag_of_words():
    synset = wn.synset('dog.n.1')
    print(synset)
    bag_of_words = lesk.synset_to_bag_of_words(synset)
    print(bag_of_words)
