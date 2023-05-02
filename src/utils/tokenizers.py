from typing import Any


class SpaCyTokenizer(object):
    def __init__(self, nlp: Any):
        self.nlp = nlp

    def __call__(self, document: str):
        tokens = self.nlp(document)

        tokens = [token.text for token in tokens]
        return tokens

        #doc = self.nlp.tokenizer(' '.join(document))
        #return [token.text for token in doc]