from pathlib import Path
from loguru import logger
from src.mir_survey_utils.survey_validators.condition_survey_validator import ConditionSurveyValidator
from src.mir_survey_utils.utils.build_checkpoint_to_survey_item_map import build_checkpoint_to_survey_item_map


if __name__ == '__main__':

    #survey_path = Path("/home/alex/qi3/mir_datasets/surveys/preprocessed/FYS_SURVEY_REPORT_HIRONDELLE_MK2_issue_1.json")
    #survey_path = Path("/home/alex/qi3/mir_datasets/surveys/preprocessed/FYS_SURVEY_REPORT_Fountaine-Pajot-Maldives-32_issue_1.json")
    survey_path = Path(
        "/home/alex/qi3/mir_datasets/surveys/preprocessed/catsample.json")

    survey = ConditionSurveyValidator(survey_json_doc=survey_path, validate=True)

    logger.info(f"Survey {survey_path} is valid={survey.is_valid}")

    checkpoint_to_survey_item_map = build_checkpoint_to_survey_item_map(path_to_checkpoints=Path("/home/alex/qi3/nv_nlp_utils/checkpoint_json_files"))

    # fix survey according to mir format
    logger.info(f"Loaded {len(checkpoint_to_survey_item_map)} survey items")


