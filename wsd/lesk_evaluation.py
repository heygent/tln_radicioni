from itertools import chain, islice
from textwrap import dedent

from nltk import Tree
from nltk.corpus import semcor, wordnet as wn
from nltk.corpus.reader import SemcorSentence, Lemma

from wsd.lesk import lesk


def pick_a_polysemic_noun(sentence):
    index = 0
    for elem in sentence:
        is_tree = isinstance(elem, Tree)
        try:
            if is_tree and len(elem.leaves()) == 1:
                lemma = elem.label()
                word, = elem.leaves()

                if not isinstance(lemma, Lemma):
                    continue

                if lemma.synset().pos() == "n" and len(wn.synsets(word)) > 1:
                    return index, lemma
        finally:
            index += len(elem.leaves() if is_tree else elem)


def semcore_sentence_to_tokens(sentence: SemcorSentence):
    lists_of_toks = [
        e.leaves() if isinstance(e, Tree) else e for e in sentence
    ]
    return list(chain.from_iterable(lists_of_toks))


def evaluate(trials=50):
    sentences = semcor.tagged_sents(tag="sem")
    positive_trials = 0

    for tagged_sentence in islice(sentences, trials):
        try:
            index, lemma = pick_a_polysemic_noun(tagged_sentence)
        except TypeError:
            continue

        tokens = semcore_sentence_to_tokens(tagged_sentence)
        predicted_synset = lesk(tokens, index)
        is_right_synset = predicted_synset == lemma.synset()
        positive_trials += is_right_synset

        print(
            dedent(
                f"""\
                Frase:             {tokens}
                Da disambiguare:   ({index}) {tokens[index]}
                Predetto:          {predicted_synset}
                Reale:             {lemma.synset()}
                Predetto == Reale: {is_right_synset}
                ------\
                """
            )
        )

    print(
        dedent(
            f"""\
            Prove totali:  {trials}
            Prove positive: {positive_trials}
            Accuratezza: {positive_trials/trials}\
            """
        )
    )


if __name__ == "__main__":
    evaluate()
