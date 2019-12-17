from nltk import WordPunctTokenizer
from wsd import lesk
import re

SENTENCE_RE = re.compile(r'^-\s*(.*)\s*$', flags=re.M)
MARKED_WORD_RE = re.compile(r'\*\*(.*)\*\*')


def get_sentences_from_resources():
    with open("wsd/resources/sentences.txt") as sentences_file:
        sentences = sentences_file.read()

    return SENTENCE_RE.findall(sentences)


def main():
    sentences = get_sentences_from_resources()
    tokenizer = WordPunctTokenizer()

    for sentence in sentences:

        tokens = tokenizer.tokenize(sentence)
        marked_word_index = tokens.index("**")

        del tokens[marked_word_index]
        del tokens[marked_word_index + 1]

        inferred_sense = lesk.lesk(tokens, marked_word_index)

        print()
        print(sentence)
        print(inferred_sense.name())

        for lemma in inferred_sense.lemmas():
            rewritten_sentence = MARKED_WORD_RE.sub(lemma.name(), sentence)
            print(rewritten_sentence)


if __name__ == "__main__":
    main()
