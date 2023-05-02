from typing import Callable, List

from .text_helpers import remove_punctuation

class Page(object):

    def __init__(self, page: str):
        self.page = page
        self.sentences = []
        self.tokens = []
        self.page_number: int = -1
        self._current_pos = -1

    def __len__(self) -> int:
        return len(self.sentences)

    def __getitem__(self, item) -> str:
        return self.sentences[item]

    def __iter__(self):
        self._current_pos = 0
        return self

    def __next__(self) -> tuple:
        if len(self.sentences) == 0:
            raise StopIteration

        if self._current_pos < len(self.sentences):
            result = self.sentences[self._current_pos]
            self._current_pos += 1
            return result
        else:
            self._current_pos = -1
            raise StopIteration

    def build_sentences(self, sentence_builder: Callable):
        self.sentences = sentence_builder(self.page)
        self.sentences = [*self.sentences]

    def build_tokens(self, tokenizer):
        self.tokens = tokenizer(self.page)

    def remove_punctuation(self):
        remove_punctuation(text=self.page)

    def apply_pipeline(self, pipeline: Callable, apply_on_sentences: bool = True):
        self.page = pipeline(self.page)

        if apply_on_sentences == True:
            for i, sentence in enumerate(self.sentences):
                self.sentences[i] = pipeline(str(sentence))

    def drop_sentence(self, idx: int) -> None:
        self.sentences.pop(idx)

    def drop_sentences(self, idxs: List[int]) -> None:
        for i in idxs:
            self.sentences.pop(i)