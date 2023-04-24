from pathlib import Path
import os
from utils.eda_utils import (
    count_document_number_of_pages,
    count_document_number_of_images,
    get_section_text,
    count_images_per_page,
    text_from_pdf_to_txt,
    download_survey_pdf,
    get_number_of_files_in_dir,
    extract_images,
    get_files_in_dir,
    count_files_for_key
)

from utils.survey_document import SurveyDocumentBase
from utils.survey_type_enum import SurveyTypeEnum
from utils.search_utils import DROP_WORDS_FOR_CONTENTS_SEARCH

data_dir = Path("./data")
condition_surveys_dir = data_dir / "condition_surveys"

if __name__ == "__main__":
    files_out = []
    get_files_in_dir(base_dir=condition_surveys_dir,
                     file_formats=[".pdf", ".PDF"],
                     files_out=files_out)

    print(f"Total number of condition surveys {len(files_out)}")

    surveys_per_vessel_type = {}

    vessel_types = ["RIB", "SAIL-CAT", "SAIL-MONO", "Motor - Open-center console",
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
    #pages = get_section_text(pdf_path=survey,
    #                         section="SUMMARY AND VALUATION",
    #                         encoding="utf8")

    #print(f"Found {len(pages)} pages with title={section_title}")

    survey = SurveyDocumentBase(survey_file=survey,
                                survey_type=SurveyTypeEnum.CONDITION_SURVEY)


    drop_contents_words  = DROP_WORDS_FOR_CONTENTS_SEARCH + [str('"Cold mold Sample" surveyed by Ulrick Marine  - Holland, PA 18966').lower()]
    survey.parse_table_of_contents(title="TABLE OF CONTENTS",
                                   drop_words=drop_contents_words)
    #survey.parse_per_section(section_name="SUMMARY AND VALUATION")




