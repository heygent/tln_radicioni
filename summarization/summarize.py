from nltk import WordNetLemmatizer
from typing import Iterable, Dict, Set

from summarization.resources import load_babelnet_ids
from summarization.nasari import NasariVector


def document_vectors(
    tokens: Iterable[str], nasari_vectors: Dict[str, Set[NasariVector]]
):
    vectors = set()
    for token in tokens:
        if token not in nasari_vectors:
            pass
        vectors.union(nasari_vectors[token])
    return vectors
