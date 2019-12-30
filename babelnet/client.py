import os

import requests

BABELNET_BASE_URL = "https://babelnet.io/v5"


class BabelNetClient:
    def __init__(self, key=os.getenv("BABELNET_KEY")):
        if key is None:
            raise ValueError("BabelNet API key not provided.")

        self.session = requests.Session()
        self.session.params["key"] = key

    def get_synset_ids(self, lemma: str, search_lang="EN", **kwargs):
        return self.session.get(
            f"{BABELNET_BASE_URL}/getSynsetIds",
            params={"lemma": lemma, "searchLang": search_lang, **kwargs,},
        ).json()
