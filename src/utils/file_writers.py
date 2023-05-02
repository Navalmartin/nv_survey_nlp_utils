from typing import TypeVar, Callable, Union
from pathlib import Path
import json

SurveyDocumentBase = TypeVar('SurveyDocumentBase')


def read_json(filename: Path) -> dict:
    """Read the specified JSON file into
    a directory
    Parameters
    ----------
    filename: The path to the JSON file
    Returns
    -------
    An instance of dict with the properties
    described in the JSON file
    """

    with open(filename) as json_file:
        json_input = json.load(json_file)
        return json_input


def write_json(filename: Path, data: Union[list, dict]):
    with open(filename, "w") as json_file:
        json.dump(data, json_file)


def label_studio_json(survey: SurveyDocumentBase, output_file: Path,
                      sentence_builder: Callable):
    survey_sentences = []
    task_counter = 0
    for pidx in range(survey.n_pages):
        page = survey.get_page_text(pidx)
        #page = remove_punctuation()
        sentences = sentence_builder(page)
        sentences = [*sentences]

        for sentence in sentences:
            survey_sentences.append({"id": task_counter,
                                     "data": {
                                         "my_text": str(sentence),
                                         "meta_info": {"page_id": pidx,
                                                       "survey_doc_id": survey.survey_file.name}
                                     }})
            task_counter += 1

    write_json(filename=output_file, data=survey_sentences)
