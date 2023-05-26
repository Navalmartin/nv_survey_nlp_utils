from typing import List, Union
from src.mir_survey_utils.survey_validators.condition_survey_validator import ConditionSurveyValidator


def trim_finding_properties(survey: ConditionSurveyValidator,
                            finding_properties: List[str]) -> None:
    """Removes left and right spaces, then replaces existing spaces with '_'
       and converts the value  of the property to upper cas

       Parameters
       ----------
       survey
       finding_properties

       Returns
       -------

    """
    survey_findings = survey.valid_survey['findings_data']

    for i, finding in enumerate(survey_findings):

        for finding_property in finding_properties:
            attr = finding[finding_property]

            if isinstance(attr, str):
                attr = attr.upper()
                attr = attr.lstrip()
                attr = attr.rstrip()
                attr = attr.replace(" ", "_")
                finding[finding_property] = attr
                survey_findings[i] = finding
            else:
                raise ValueError(f"The property {finding_property} is not a string. "
                                 f"Only strings allowed here.")


def set_checkpoint_group_to_mir_type(survey: ConditionSurveyValidator,
                                     checkpoint_group_map: dict):
    survey_findings = survey.valid_survey['findings_data']

    not_found = []
    for i, finding in enumerate(survey_findings):

        checkpoint_item = finding['checkpoint_item']

        found = False
        for survey_item in checkpoint_group_map:
            if checkpoint_item in checkpoint_group_map[survey_item]:
                finding['checkpoint_group'] = survey_item
                survey_findings[i] = finding
                found = True
                break

        if not found:
            not_found.append(checkpoint_item)

    return not_found


def replace_checkpoint_group_name(survey: ConditionSurveyValidator,
                                  checkpoint_group_name: dict) -> int:
    survey_findings = survey.valid_survey['findings_data']

    updated = 0
    for i, finding in enumerate(survey_findings):

        if finding['checkpoint_item'] in checkpoint_group_name:

            finding['checkpoint_item'] = checkpoint_group_name[finding['checkpoint_item']]
            survey_findings[i] = finding
            updated += 1

    return updated


def set_checkpoint_item_to_checkpoint_group(survey: ConditionSurveyValidator,
                                            checkpoint_item_to_checkpoint_group: dict) -> int:
    survey_findings = survey.valid_survey['findings_data']

    updated = 0
    for i, finding in enumerate(survey_findings):
        if finding['checkpoint_item'] in checkpoint_item_to_checkpoint_group:
            finding['checkpoint_group'] = checkpoint_item_to_checkpoint_group[finding['checkpoint_item']]
            survey_findings[i] = finding
            updated += 1

    return updated


def replace_findings_severity(survey: ConditionSurveyValidator,
                              old_severity_value: str,
                              new_severity_value: str) -> int:
    survey_findings = survey.valid_survey['findings_data']
    old_severity_value_copy = old_severity_value.upper()
    new_severity_value_copy = new_severity_value.upper()

    updated = 0
    for i, finding in enumerate(survey_findings):

        severity = finding['severity']

        if severity == old_severity_value_copy:
            finding['severity'] = new_severity_value_copy

            survey_findings[i] = finding
            updated += 1

    return updated


def remove_findings(survey: ConditionSurveyValidator,
                    checkpoint_items: List[str]=None,
                    checkpoint_ids: List[Union[str, int]] = None) -> int:
    survey_findings = survey.valid_survey['findings_data']

    if checkpoint_items is None and checkpoint_ids is None:
        updated = len(survey_findings)
        survey.valid_survey['findings_data'] = []
        return updated

    updated = 0
    remove = []
    for i, finding in enumerate(survey_findings):

        survey_checkpoint_item = finding['checkpoint_item']
        id = finding['id']

        if checkpoint_items is not None and survey_checkpoint_item in checkpoint_items:
            remove.append(i)
            updated += 1
        elif checkpoint_ids is not None and id in checkpoint_ids:
            remove.append(i)
            updated += 1

    survey.valid_survey['findings_data'] = [finding for i, finding in enumerate(survey_findings) if i not in remove]
    return updated


def remove_property(survey: ConditionSurveyValidator,
                    property_name: str) -> int:

    survey_findings = survey.valid_survey['findings_data']
    updated = 0
    remove = []
    for i, finding in enumerate(survey_findings):

        if property_name in finding:
            finding.pop(property_name)
            survey_findings[i] = finding
            updated += 1

    return updated










