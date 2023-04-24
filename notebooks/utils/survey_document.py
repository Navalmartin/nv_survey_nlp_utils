from pathlib import Path
from pdfminer.high_level import extract_text
from typing import List

from .survey_type_enum import SurveyTypeEnum
from .eda_utils import get_section_text
from .search_utils import DROP_WORDS_FOR_CONTENTS_SEARCH


class SurveyDocumentBase(object):

    def __init__(self, survey_file: Path,
                 survey_type: SurveyTypeEnum):
        self.survey_file = survey_file
        self.survey_type = survey_type
        self.survey_text: str = None
        self.sections: dict = {}
        self.contents = []

    def read_as_text_from(self) -> None:
        self.survey_text = extract_text(self.survey_file)

    def parse_table_of_contents(self, title: str = "Table of Contents",
                                delimiter: str = '\n',
                                minimum_characters: int = 2,
                                drop_words: List[str] = DROP_WORDS_FOR_CONTENTS_SEARCH):
        pages = get_section_text(pdf_path=self.survey_file, section=title)

        for page in pages:
            # print(page[1])
            page_data = page[1].split(delimiter)
            for text in page_data:
                text = text.replace('.', '')

                if len(text) <= minimum_characters:
                    continue

                if text.lower() in drop_words:
                    continue

                print(text)

    def parse_per_section(self, section_name: str):
        pages = get_section_text(pdf_path=self.survey_file, section=section_name)

        for i, page in enumerate(pages):
            try:
                rect = page[0][0]
                print(page[1])
            except ValueError as e:
                print(f"Exception message for page {i}")
                print(str(e))
                continue
