from typing import List,  Dict, Tuple
import numpy as np
from collections import defaultdict


def replace_defect_label(defects: List, old_to_new_defect_label_map: Dict):
    for i, item in enumerate(defects):
        defect_labels = item['defect_labels']

        for j, dl in enumerate(defect_labels):
            if dl in old_to_new_defect_label_map:
                defect_labels[j] = old_to_new_defect_label_map[dl]
        item['defect_labels'] = defect_labels
        defects[i] = item


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




def get_finding_recommendation_word_embeddings(defects: List):
    pass
