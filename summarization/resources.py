import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

RESOURCES_PATH = Path(__file__).parent / "resources"
TEXTS_PATH = RESOURCES_PATH / "texts"
BN_IDS_PATH = RESOURCES_PATH / "babelnet_ids.json"


@dataclass
class TextResource:
    title: str
    paragraphs: List[str]
    text: str

    def __str__(self):
        return self.text

    @classmethod
    def parse(cls, text):
        paragraphs = []

        for line in text.splitlines(keepends=False):
            if line != "" and line[0] != "#":
                paragraphs.append(line)

        title = paragraphs.pop(0)

        return cls(title, paragraphs, text)


def load_text_resources():
    for file in TEXTS_PATH.iterdir():
        yield TextResource.parse(file.read_text())


def load_babelnet_ids():
    if not BN_IDS_PATH.exists():
        return {}

    with BN_IDS_PATH.open() as babelnet_ids_file:
        return json.load(babelnet_ids_file)


def save_babelnet_ids(ids):
    with BN_IDS_PATH.open("w+") as babelnet_ids_file:
        json.dump(ids, babelnet_ids_file, indent=4)
