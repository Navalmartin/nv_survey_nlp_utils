from pathlib import Path
from pdfminer.high_level import extract_text
from typing import List, Callable, Union
import fitz
from .survey_page import Page
from .survey_section import ServeySection
from .survey_type_enum import SurveyTypeEnum
from .file_utils import get_section_text
from .search_utils import DROP_WORDS_FOR_CONTENTS_SEARCH


class SurveyDocumentBase(object):

    def __init__(self, survey_file: Path,
                 survey_type: SurveyTypeEnum):
        self.survey_file = survey_file
        self.survey_type = survey_type
        self.survey_text: str = None
        self.sections: dict = {}
        self.contents = []
        self.survey_doc_metadata = None
        self.n_pages = 0
        self._current_pos = -1

    def __len__(self) -> int:
        return len(self.contents)

    def __iter__(self):
        self._current_pos = 0
        return self

    def __next__(self) -> tuple:
        if len(self.contents) == 0:
            raise StopIteration

        if self._current_pos < len(self.contents):
            section = self.contents[self._current_pos]
            result = self.sections[section]
            self._current_pos += 1
            return section, result
        else:
            self._current_pos = -1
            raise StopIteration

    def close(self) -> None:
        self.sections: dict = {}
        self.contents = []

    def read_as_text_from(self) -> None:
        self.survey_text = extract_text(self.survey_file)

    def num_pages_per_section(self, section_name: str) -> int:
        if not section_name in self.contents:
            return 0

        return len(self.sections[section_name])



    """
    def parse_document(self, toc_name: str,
                       toc_delimiter: str = '\n',
                       minimum_characters: int = 2,
                       drop_words: List[str] = DROP_WORDS_FOR_CONTENTS_SEARCH) -> None:

        self.close()

        # get the table of contents
        self.parse_table_of_contents(title=toc_name, delimiter=toc_delimiter,
                                     minimum_characters=minimum_characters, drop_words=drop_words)

        if len(self.contents) == 0:
            raise ValueError("Contents are empty. The document was not parsed correctly")

        for section in self.contents:
            self.parse_per_section(section_name=section)
    """

    def parse_table_of_contents(self, simple: bool = True) -> List[List]:
        """Parser the table of contents for the document.
        This is just a wrapper to the pymupdf.Document.get_toc()
        for more details, see here:
        https://pymupdf.readthedocs.io/en/latest/document.html#Document.get_toc

        Parameters
        ----------
        simple:

        Returns
        -------

        """
        with fitz.open(self.survey_file) as pdf:
            self.contents = pdf.get_toc(simple)
            self.n_pages = pdf.page_count
            self.survey_doc_metadata = pdf.metadata
        return self.contents

    def get_page_text(self, page_id: Union[int, tuple], search_for_text: str = None):
        """Get the text associated with the page.

        Parameters
        ----------
        page_id
        search_for_text

        Returns
        -------

        """

        with fitz.open(self.survey_file) as pdf:
            page = pdf.load_page(page_id)

            if search_for_text is not None:
                # we want to do a search in the
                # page with the given text
                found = page.search_for(search_for_text)

                if len(found) != 0:
                    return page
                else:
                    return None

            return page.get_text()

    def get_pages(self, page_idx_start: int, page_idx_end: int):

        page_ids = [i for i in range(page_idx_start, page_idx_end + 1 , 1)]
        pages = []
        with fitz.open(self.survey_file) as pdf:

            for pidx in page_ids:
                page = pdf.load_page(pidx)
                pages.append(page.get_text())

            return pages

    def get_pages_in_list(self, page_idxs: List[int]):

        pages = []
        with fitz.open(self.survey_file) as pdf:

            for pidx in page_idxs:
                page = pdf.load_page(pidx)
                pages.append([page.get_text(), pidx])

            return pages

    def parse_document(self):
        self.close()

    def parse_per_section(self, section_name: str):

        if section_name not in self.contents:
            raise ValueError(f"Invalid section name={section_name}. Not in t {self.contents}")

        # read the pages of the section
        pages = get_section_text(pdf_path=self.survey_file, section=section_name)

        if section_name not in self.sections:
            self.sections[section_name] = ServeySection(section_name=section_name)

        for i, page in enumerate(pages):
            try:
                rect = page[0][0]
                self.sections[section_name].add_page(page=page[1])
            except ValueError as e:
                print(f"Exception message for page {i}")
                print(str(e))
                continue

    def apply_pipeline(self, pipeline: Callable) -> None:

        for section in self.sections:
            section.apply_pipeline(pipeline)

    def get_survey_items(self, survey_items_names: List[str]):
        pass
