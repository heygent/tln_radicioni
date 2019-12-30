import logging

from summarization import nasari
from pprint import pprint

logging.basicConfig(level="INFO")


def main():
    with open("resources/dd-small-nasari-15.txt") as nasari_file:
        lemmas = nasari.build_lemma_index(nasari.read_nasari_resource(nasari_file))

    pprint(lemmas)


main()
