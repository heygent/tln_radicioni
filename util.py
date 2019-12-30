from typing import Mapping, Callable, TypeVar, Dict

import nltk
from toolz import curry

K = TypeVar("K")
V = TypeVar("V")
N = TypeVar("N")


@curry
def merge_with(
    fn: Callable[[V, V], N], a: Mapping[K, V], b: Mapping[K, V]
) -> Dict[K, N]:
    return {k: fn(a[k], b[k]) for k in a.keys() & b.keys()}


_STOPWORDS = set(nltk.corpus.stopwords.words("english"))


def is_stopword(token: str):
    return not token[0].isalnum() and token not in _STOPWORDS


def words(text: str):
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        for token in nltk.word_tokenize(sentence):
            if not is_stopword(token):
                yield token
