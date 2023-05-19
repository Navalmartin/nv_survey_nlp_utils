import spacy
from typing import Any


class SpaCySentenceBuilder(object):

    def __init__(self, nlp: Any):
        self.nlp = nlp

    def __call__(self, document: str):
        doc = self.nlp(document)
        return doc.sents