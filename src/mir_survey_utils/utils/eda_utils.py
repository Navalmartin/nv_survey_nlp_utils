from typing import List, Set, Dict, Tuple
import numpy as np


def get_unique_defect_labels(defects: List) -> Set:
    unique_defects = set()
    for item in defects:
        defect_labels = item['defect_labels']
        for dl in defect_labels:
            unique_defects.add(dl)
    return unique_defects


def replace_defect_label(defects: List, old_to_new_defect_label_map: Dict):
    for i, item in enumerate(defects):
        defect_labels = item['defect_labels']

        for j, dl in enumerate(defect_labels):
            if dl in old_to_new_defect_label_map:
                defect_labels[j] = old_to_new_defect_label_map[dl]
        item['defect_labels'] = defect_labels
        defects[i] = item


def get_defects_counter(defects: List) -> Dict:
    """Get a map with the defect label and how many times
    this defect has occured

    Parameters
    ----------
    defects: List defect

    Returns
    -------

    """
    counter_map = {}

    for item in defects:
        defect_labels = item['defect_labels']

        for dl in defect_labels:
            if dl in counter_map:
                counter_map[dl] += 1
            else:
                counter_map[dl] = 1

    return counter_map


def get_finding_recommendation_map(defects: List) -> Dict:
    recommendation_map = {}

    for item in defects:

        finding = item['finding']
        recommendation = item['recommendation_description']

        if finding in recommendation_map:
            recommendation_map[finding].append(recommendation)
        else:
            recommendation_map[finding] = [recommendation]

    return recommendation_map


def get_number_of_defects_per_survey_item_map(defects: List) -> Dict:
    counter_map = {}

    for item in defects:
        defect_labels = item['defect_labels']
        survey_item_type = item['survey_item_type']

        if survey_item_type not in counter_map:
            counter_map[survey_item_type] = 0

        for _ in defect_labels:
            counter_map[survey_item_type] += 1

    return counter_map


def get_number_of_defects_per_checkpoint_map(defects: List) -> Dict:
    counter_map = {}

    for item in defects:
        defect_labels = item['defect_labels']
        checkpoint_type = item['checkpoint_type']

        if checkpoint_type not in counter_map:
            counter_map[checkpoint_type] = 0

        for _ in defect_labels:
            counter_map[checkpoint_type] += 1

    return counter_map


def prepare_counter_map_for_plot(data_map: Dict, top: int,
                                 order: str="normal") -> Tuple[List[str], List[int]]:
    names: List[str] = []
    counters: List[int] = []

    top = top
    counter = 0

    if order == "normal":

        for item in data_map:
            names.append(item)
            counters.append(data_map[item])
            counter += 1

            if top is not None and counter >= top:
                break
    else:

        for item in reversed(data_map):
            names.append(item)
            counters.append(data_map[item])
            counter += 1

            if top is not None and counter >= top:
                break

    return names, counters


def get_defects_per_survey(defects: Dict, unique_defects: Set):

    survey_defects = {}
    unique_defects_list = list(unique_defects)

    for doc in defects:
        survey_doc = doc['survey_doc_id']

        defects = doc['defect_labels']

        if survey_doc not in survey_defects:
            survey_defects[survey_doc] = []

        for defect in defects:
            col = unique_defects_list.index(defect)

            severity = doc['defect_degree']

            if severity == 'MODERATE':
                severity = 0.5
            elif severity == 'MINOR':
                severity = 0.3
            elif severity == 'HIGH':
                severity = 0.95
            else:
                raise ValueError(f"Severity scale {severity} not found")

            survey_defects[survey_doc].append((col, severity))
    return survey_defects


def prepare_checkpoint_defect_matrix(matrix: np.ndarray, survey_defects: Dict):

    row_idx_to_survey_doc = {}

    # set up the matrix
    for row, doc in enumerate(survey_defects):

        row_idx_to_survey_doc[row] = doc

        cols = survey_defects[doc]

        for col in cols:
            idx = col[0]
            val = col[1]
            matrix[row][idx] = val

    return row_idx_to_survey_doc


def get_findings_with_label(defects: List[Dict], labels: List[str]) -> List[Dict]:
    """Filter the defects that have a defect label in the labels attribute

    Parameters
    ----------
    defects
    labels

    Returns
    -------

    """
    found: List[Dict] = []
    for finding in defects:
        defect_labels = finding['defect_labels']
        for label in defect_labels:
            if label in labels:
                found.append(finding)

    return found


def get_finding_recommendation_word_embeddings(defects: List):
    pass
