from typing import List, Callable
from .survey_page import Page


class ServeySection(object):
    def __init__(self, section_name: str):
        self.section_name = section_name
        self.pages: List[Page] = []
        self._current_pos = -1

    def __len__(self) -> int:
        return len(self.pages)

    def __getitem__(self, item) -> Page:
        return self.pages[item]

    def __iter__(self):
        self._current_pos = 0
        return self

    def __next__(self) -> tuple:
        if len(self.pages) == 0:
            raise StopIteration

        if self._current_pos < len(self.pages):
            result = self.pages[self._current_pos]
            self._current_pos += 1
            return result
        else:
            self._current_pos = -1
            raise StopIteration

    def add_page(self, page: str) -> None:
        self.pages.append(Page(page=page))

    def build_section_sentences(self, sentence_builder: Callable):
        for page in self.pages:
            page.build_sentences(sentence_builder=sentence_builder)

    def remove_punctuation(self):
        for page in self.pages:
            page.remove_punctuation()

    def apply_pipeline(self, pipeline: Callable):

        for page in self.pages:
            page.apply_pipeline(pipeline)
