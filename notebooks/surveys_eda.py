from pathlib import Path
import spacy
from src.mir_survey_utils.utils import (
    count_document_number_of_pages,
    count_document_number_of_images,
    get_files_in_dir,
    count_files_for_key
)

from src.mir_survey_utils.utils import SurveyDocumentBase
from src.mir_survey_utils.utils import SurveyTypeEnum
from src.mir_survey_utils.utils import DROP_WORDS_FOR_CONTENTS_SEARCH
from src.mir_survey_utils.utils import SpaCySentenceBuilder
from src.mir_survey_utils.utils import TextPipeline
from src.mir_survey_utils.utils import (ReplaceTask, LStrip, RStrip, RemovePunctuation)

data_dir = Path("./data")
condition_surveys_dir = data_dir / "condition_surveys"

if __name__ == "__main__":
    files_out = []
    get_files_in_dir(base_dir=condition_surveys_dir,
                     file_formats=[".pdf", ".PDF"],
                     files_out=files_out)

    print(f"Total number of condition surveys {len(files_out)}")

    surveys_per_vessel_type = {}

    vessel_types = ["RIB", "SAIL-CAT", "SAIL-MONO",
                    "Motor - Open-center console",
                    "Super+mega", "Motor cabin"]

    for key in vessel_types:
        vessel_type_surveys = count_files_for_key(files_out, key=key)

        if len(vessel_type_surveys) != 0:
            surveys_per_vessel_type.update(vessel_type_surveys)

    print("Condition surveys per vessel type")

    for item in surveys_per_vessel_type:
        print(f"Vessel type={item} total surveys={surveys_per_vessel_type[item]}")

    # count number of pages
    total_number = 0
    for pdf_path in files_out:
        fname, num_pages = count_document_number_of_pages(pdf_path)
        print(f"Number of pages in {fname}: {num_pages}")
        total_number += num_pages

    print(f"Average number of pages per survey={float(total_number) / len(files_out)}")

    total_number_of_images = 0
    for pdf_path in files_out:
        num_images = count_document_number_of_images(pdf_path)
        print(f"Number of images in {pdf_path.name}: {num_images}")
        total_number_of_images += num_images

    print(f"Average number of images per survey={float(total_number_of_images) / len(files_out)}")

    survey = Path(
        "/home/alex/qi3/nv_nlp_utils/notebooks/data/condition_surveys/Motor - Open-center console/coldsample.pdf")

    section_title = "SUMMARY AND VALUATION"
    survey = SurveyDocumentBase(survey_file=survey,
                                survey_type=SurveyTypeEnum.CONDITION_SURVEY)

    drop_contents_words = DROP_WORDS_FOR_CONTENTS_SEARCH + [str('"Cold mold Sample" surveyed by Ulrick Marine  - Holland, PA 18966').lower()]

    # parse the document
    survey.parse_document(toc_name="TABLE OF CONTENTS",
                          drop_words=drop_contents_words)

    nlp = spacy.load('en_core_web_sm')
    sentence_builder = SpaCySentenceBuilder(nlp=nlp)
    # loop over the sections of the document
    for section_name, section in survey:
        print(f"Section={section_name}, number of pages={len(section)}")

        if section_name == "INTRODUCTION":
            section.remove_punctuation()
            section.build_section_sentences(sentence_builder)

    section_name = "INTRODUCTION"
    introduction = survey.sections[section_name]

    section_pipeline = TextPipeline(tasks=[ReplaceTask(replace_with="", text_to_replace="."),
                                           RemovePunctuation(),
                                           LStrip(), RStrip()])

    introduction.apply_pipeline(pipeline=section_pipeline)
    print(f"Number of pages in section={section_name}, {len(introduction)}")

    page_id = 1
    page = introduction[page_id]
    print(f"Looking at page {page_id}")

    '''
    remove_sentences = []
    for i, sentence in enumerate(page):
        if sentence == " ":
            remove_sentences.append(i)
    
    page.drop_sentences(remove_sentences)
    '''

    for i, sentence in enumerate(page):

        if len(sentence) != 0:
            print(f"Sentence {i}= {sentence}")


