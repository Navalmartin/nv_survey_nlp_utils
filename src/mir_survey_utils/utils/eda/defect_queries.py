from typing import List, Dict, Set
from collections import defaultdict


def get_defect_labels_for_survey_items(defects: List[Dict],
                                       survey_items: List[str],
                                       with_defect_counter: bool = True) -> Dict:

    #import pdb
    #pdb.set_trace()

    if with_defect_counter:
        query_result = {}

        for defect in defects:
            survey_item_type = defect['survey_item_type']

            if survey_item_type in survey_items:

                if survey_item_type not in query_result:
                    query_result[survey_item_type] = []

                current_labels = query_result[survey_item_type]

                if len(current_labels) == 0:
                    for label in defect['defect_labels']:
                        query_result[survey_item_type].append({label: 1})
                else:

                    for label in defect['defect_labels']:
                        for i, item in enumerate(current_labels):
                            if label in item:
                                item[label] += 1
                            else:
                                item[label] = 1

                            current_labels[i] = item
                    query_result[survey_item_type] = current_labels

        return query_result

    query_result = defaultdict(set)
    for defect in defects:
        survey_item_type = defect['survey_item_type']

        if survey_item_type in survey_items:
            query_result[survey_item_type].add(label for label in defect['defect_labels'])

    return query_result


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


def get_defects_label_counter(defects: List) -> Dict:
    """Get a map with the defect label and how many times
    this defect has occurred

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


def get_defect_severity_counter(defects: List[Dict]) -> Dict:
    """Returns a dictionary with the counter of the
    defect degree

    Parameters
    ----------
    defects

    Returns
    -------

    """

    counter_map = {'HIGH': 0,
                   'MODERATE': 0,
                   'MINOR': 0}

    for item in defects:
        defect_degree = item['defect_degree']

        counter_map[defect_degree] += 1

    return counter_map


def get_vessel_type_counter(defects: List[Dict]) -> Dict:


    survey_to_vessel_type_map = {}
    for defect in defects:

        vessel_type = defect['vessel_type']
        survey_doc_id = defect['survey_doc_id']

        if survey_doc_id in survey_to_vessel_type_map:
            continue

        survey_to_vessel_type_map[survey_doc_id] = vessel_type

    single_hull_counter = 0
    catamaran_counter = 0
    trimaran_counter = 0
    rib_counter = 0

    for survey_doc in survey_to_vessel_type_map:
        vessel_type = survey_to_vessel_type_map[survey_doc]

        if vessel_type == 'single_hull' or vessel_type == 'single hull':
            single_hull_counter += 1

        elif vessel_type == 'catamaran':
            catamaran_counter += 1

        elif vessel_type == 'trimaran':
            trimaran_counter += 1

        elif vessel_type == 'rib':
            rib_counter += 1

        else:
            print(vessel_type)

    return {'single_hull': single_hull_counter, 'catamaran': catamaran_counter,
            'rib': rib_counter, 'trimaran': trimaran_counter}


def get_unique_defect_labels(defects: List) -> Set:
    unique_defects = set()
    for item in defects:
        defect_labels = item['defect_labels']
        for dl in defect_labels:
            unique_defects.add(dl)
    return unique_defects