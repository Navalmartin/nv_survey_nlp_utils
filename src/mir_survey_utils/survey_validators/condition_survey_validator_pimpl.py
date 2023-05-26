from pathlib import Path
import json
from loguru import logger
from typing import Union, List

from src.mir_survey_utils.schemata.survey_schemas.engine_data_schema import Engine, EngineEntry
from src.mir_survey_utils.schemata.survey_schemas.vessel_data_schema import VesselDim, VesselDataSchema
from src.mir_survey_utils.schemata.survey_schemas.survey_data_schema import SurveyDataSchema, SeverityScale
from src.mir_survey_utils.schemata.survey_schemas.finding_data_schema import FindingDataSchema
from src.mir_survey_utils.schemata.survey_schemas.survey_item_data_schema import SurveyItemDataSchema
from src.mir_survey_utils.schemata.survey_schemas.checkpoint_data_schema import CheckpointDataSchema

OK = "OK"
NOT_OK = "NOT_OK"


class ConditionSurveyValidatorPimpl(object):
    def __init__(self, survey_json_doc: Path = None, validate: bool = False):
        self.survey = None
        self.source: Path = survey_json_doc
        self.is_valid: bool = False
        self.valid_survey = {}

        if survey_json_doc is not None:
            self._load(source=self.source)

            if validate:
                self._validate()

    def _load(self, source: Path):

        with open(source, 'r') as f:
            self.survey = json.load(f)
            self.source = source

    def _validate(self) -> Union[OK, NOT_OK]:
        try:

            validate_survey_data = self._validate_survey_data()

            if validate_survey_data != OK:
                raise ValueError("Survey data was not validated")

            validate_vessel_data = self._validate_vessel_data()

            if validate_vessel_data != OK:
                raise ValueError("Vessel data was not validated")

            validate_engine = self._validate_engine()

            if validate_engine != OK:
                raise ValueError("Vessel engine was not validated")

            validate_survey_items_data = self._validate_survey_items_data()

            if validate_survey_items_data != OK:
                raise ValueError("Survey validate_survey_items_data not validated")

            validate_checkpoint_data = self._validate_survey_checkpoints_data()

            if validate_checkpoint_data != OK:
                raise ValueError("Survey checkpoint_synopsis_data not validated")

            validate_findings = self._validate_findings()

            if validate_findings != OK:
                raise ValueError("Survey findings not validated")

            self.is_valid = True
        except Exception as e:

            logger.error(f"An error occurred whilst validating survey document {str(e)}")
            self.is_valid = False
            return NOT_OK

    def _validate_survey_data(self) -> Union[OK, NOT_OK]:
        try:
            logger.info("Validating survey data...")
            survey_data = self.survey["survey_data"]

            severity_scales = survey_data["severity_scales"]
            severity_scales_arr: List[SeverityScale] = []

            for item in severity_scales:

                if 'type' not in item:
                    raise ValueError("'type' not in keys. Invalid format")

                if 'explanation' not in item:
                    raise ValueError("'explanation' not in keys. Invalid format")

                severity_scales_arr.append(SeverityScale(**{"name": item["type"],
                                                            "explanation": item["explanation"]}))

            survey_data = SurveyDataSchema(**{"severity_scales": severity_scales_arr,
                                              "survey_doc_id": survey_data["survey_doc_id"],
                                              "survey_type": survey_data["survey_type"],
                                              "survey_summary": survey_data["survey_summary"],
                                              "survey_purpose": survey_data["survey_purpose"]
                                              })

            self.valid_survey["survey_data"] = survey_data.dict()
            logger.info("Validating survey data. DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating survey data {str(e)}")
            return NOT_OK

    def _validate_vessel_data(self) -> Union[OK, NOT_OK]:
        try:
            logger.info("Validating vessel_data...")
            vessel_data = self.survey["vessel_data"]

            survey_dimensions = vessel_data["dimensions"]
            dimensions: List[VesselDim] = []

            for item in survey_dimensions:

                if 'units' not in item:
                    raise ValueError("'units' not in keys. Invalid format")

                keys = list(item.keys())
                keys.remove("units")

                if len(keys) != 1:
                    raise ValueError(f"Unrecognised format for item in survey dimensions. Item was={item}")

                dimensions.append(VesselDim(**{"metric": item["units"],
                                               "name": keys[0],
                                               "dimension": item[keys[0]]}))

            vessel_data = VesselDataSchema(**{"vessel_dimensions": dimensions,
                                              "vessel_name": vessel_data["vessel_name"],
                                              "hull_material": vessel_data["hull_material"],
                                              "hin": vessel_data["hin"],
                                              "sea_category": vessel_data["sea_category"],
                                              "vessel_type": vessel_data["vessel_type"],
                                              "model_year": vessel_data["model_year"],
                                              "survey_vessel_type": vessel_data["survey_vessel_type"],
                                              "survey_vessel_model": vessel_data["survey_vessel_model"],
                                              "ssr": vessel_data["ssr"],
                                              "max_n_persons": vessel_data["max_n_persons"],
                                              "vessel_usage_type": vessel_data["vessel_usage_type"]})

            self.valid_survey["vessel_data"] = vessel_data.dict()
            logger.info("Validating vessel_data.DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating vessel data {str(e)}")
            return NOT_OK

    def _validate_engine(self) -> Union[OK, NOT_OK]:

        try:
            logger.info("Validating engine...")
            vessel_data = self.survey["vessel_data"]

            if 'engine' not in vessel_data:
                raise ValueError("'engine' not in keys. Invalid format")

            engine = vessel_data["engine"]

            # how many engines we have
            n_engines = engine['number_of_engines']

            if n_engines <= 0:
                raise ValueError(f"Document has zero number of engines")

            engines: List[EngineEntry] = []

            for engine in engine['engines']:
                engines.append(EngineEntry(**engine))

            if len(engines) != n_engines:
                raise ValueError(f"The specified number of engines {n_engines} does "
                                 f"not equal the entries found {len(engines)}")

            vessel_engine = Engine(**{"number_of_engines": n_engines,
                                      "engines": engines})

            self.valid_survey["vessel_engine"] = vessel_engine.dict()
            logger.info("Validating engine. DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating engine {str(e)}")
            return NOT_OK

    def _validate_findings(self):

        try:
            logger.info("Validating findings...")
            findings = self.survey['findings_data']

            for finding in findings:
                finding = FindingDataSchema(**finding)

            self.valid_survey['findings_data'] = findings
            logger.info("Validating findings. DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating findings. {str(e)}")
            return NOT_OK

    def _validate_survey_checkpoints_data(self):

        try:
            logger.info("Validating survey checkpoint_synopsis_data...")
            checkpoint_synopsis_data = self.survey['checkpoint_synopsis_data']

            if checkpoint_synopsis_data is None:
                checkpoint_synopsis_data = []

            for survey_item in checkpoint_synopsis_data:
                survey_item = CheckpointDataSchema(**survey_item)

            self.valid_survey['checkpoint_synopsis_data'] = checkpoint_synopsis_data
            logger.info("Validating survey checkpoint_synopsis_data. DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating checkpoint_synopsis_data. {str(e)}")
            return NOT_OK

    def _validate_survey_items_data(self):

        try:
            logger.info("Validating survey items data...")
            survey_items_data = self.survey['survey_items_data']

            if survey_items_data is None:
                survey_items_data = []

            for survey_item in survey_items_data:
                survey_item = SurveyItemDataSchema(**survey_item)

            self.valid_survey['survey_items_data'] = survey_items_data
            logger.info("Validating survey items data. DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating survey_items_data. {str(e)}")
            return NOT_OK
