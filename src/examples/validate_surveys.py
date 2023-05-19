from pathlib import Path
from loguru import logger
from src.mir_survey_utils.survey_validators.condition_survey_validator import ConditionSurveyValidator
if __name__ == '__main__':

    survey_path = Path("/home/alex/qi3/mir_datasets/surveys/clean/FYS_SURVEY_REPORT_HIRONDELLE_MK2_issue_1.json")

    survey = ConditionSurveyValidator(survey_json_doc=survey_path, validate=True)

    logger.info(f"Survey {survey_path} is valid={survey.is_valid}")


