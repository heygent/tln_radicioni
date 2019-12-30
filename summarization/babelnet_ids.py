from typing import Iterable, List, Dict

from nltk import WordNetLemmatizer

from babelnet import BabelNetClient
from summarization import resources
from util import words


def fetch_lemmas_ids(
    client: BabelNetClient, lemmas: Iterable[str], out: Dict[str, List[str]]
):
    for lemma in lemmas:
        if lemma in out:
            continue
        synsets_data = client.get_synset_ids(lemma)
        out[lemma] = [synset_data["id"] for synset_data in synsets_data]


def main():
    babelnet_ids = resources.load_babelnet_ids()
    babelnet_client = BabelNetClient()
    lemmatizer = WordNetLemmatizer()

    for resource in resources.load_text_resources():
        print(f"\nTitolo: {resource.title}")

        should_load_ids = None
        while should_load_ids not in ("Y", "n", ""):
            should_load_ids = input(
                "Scaricare gli ID dei synset delle parole nella risorsa? [Y/n] "
            )

        if should_load_ids in "Y":
            fetch_lemmas_ids(
                babelnet_client,
                map(lemmatizer.lemmatize, words(resource.text)),
                babelnet_ids,
            )

    resources.save_babelnet_ids(babelnet_ids)


if __name__ == "__main__":
    main()
