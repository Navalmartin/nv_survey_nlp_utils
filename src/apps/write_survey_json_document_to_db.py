import dotenv
import asyncio
from pathlib import Path
from loguru import logger
from typing import List
from navalmartin_mir_db_utils.dbs import MongoDBSession
from navalmartin_mir_db_utils.crud.mongodb_crud_ops import CreateEntityCRUDAPI

from src.mir_survey_utils.utils.file_io import read_json
from src.mir_survey_utils.schemata.db_schemas.defect_schema import DefectSchema
from src.mir_survey_utils.survey_validators.condition_survey_validator import ConditionSurveyValidator


DOTENV_PATH = Path("/home/alex/qi3/dotenvs/.env")

#SURVEY_FILENAME = "FYS_SURVEY_REPORT_HIRONDELLE_MK2_issue_1.json"
#SURVEY_FILENAME = "FYS_SURVEY_REPORT_Fountaine-Pajot-Maldives-32_issue_1.json"
#SURVEY_FILENAME = "catsample.json"
#SURVEY_FILENAME = "coldsample.json"
#SURVEY_FILENAME = "atlanta.json"
#SURVEY_FILENAME = "regal_commodore_272.json"
#SURVEY_FILENAME = "sample_carver_310_survey.json"
#SURVEY_FILENAME = "sample_silverton_410_survey.json"
SURVEY_FILENAME = "FYS_SURVEY_REPORT_MOODY_29_issue_1.json"

ALIGNED_PATH = Path("/home/alex/qi3/mir_datasets/surveys/aligned")
CLEANED_PATH = Path("/home/alex/qi3/mir_datasets/surveys/cleaned")

SURVEY_JSON_DOC = ALIGNED_PATH / SURVEY_FILENAME


async def insert_findings(findings: List, db_session: MongoDBSession):

    response = await CreateEntityCRUDAPI.insert_many(data=findings,
                                                     db_session=db_session,
                                                     collection_name="defects")
    return response


if __name__ == '__main__':


    try:
        dotenv.load_dotenv(DOTENV_PATH)

        # db session
        db_session = MongoDBSession()

        survey_json = read_json(filename=SURVEY_JSON_DOC)

        survey = ConditionSurveyValidator(survey_json_doc=SURVEY_JSON_DOC,
                                              validate=True)

        survey_data = survey.valid_survey["survey_data"]
        survey_doc_id = survey_data['survey_doc_id']
            # get the findings
        findings = survey.valid_survey['findings_data']

        findings_array = []
        for finding in findings:

                if finding['defect_labels'] is None:
                    logger.warning(f"For {finding['id']} defect_labels is None")
                    continue

                finding.pop('id')

                finding['vessel_type'] = survey['vessel_data']['vessel_type']
                finding['survey_doc_id'] = survey_doc_id
                defect = DefectSchema(**finding)
                #defect.updated_at = str(defect.updated_at)
                #defect.created_at = str(defect.created_at)
                findings_array.append(defect.dict())

        response = asyncio.run(insert_findings(findings_array, db_session=db_session))
        logger.info(f"Insert response={response}")

        # save the cleaned survey
        filename = survey.filename
        survey.save(filename=CLEANED_PATH / f"{filename}")
    except Exception as e:
        logger.error(f"An error occurred whilst inserting survey {SURVEY_JSON_DOC}")
        logger.error(f"Exception message {str(e)}")




