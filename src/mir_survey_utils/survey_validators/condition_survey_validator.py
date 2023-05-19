from pathlib import Path
import json
from loguru import logger
from typing import Union, List
from pydantic import Field
from src.mir_survey_utils.survey_schemas.engine_schema import Engine, EngineEntry
from src.mir_survey_utils.survey_schemas.vessel_data_schema import VesselDim, VesselDataSchema
from src.mir_survey_utils.survey_schemas.survey_data_schema import SurveyDataSchema, SeverityScale

OK = "OK"
NOT_OK = "NOT_OK"


class ConditionSurveyValidator(object):

    def __init__(self, survey_json_doc: Path = None, validate: bool = False):
        self.survey = None
        self.source: Path = survey_json_doc
        self.is_valid: bool = False
        self.valid_survey = {}

        if survey_json_doc is not None:
            self.load(source=self.source)

            if validate:
                self.validate()

    def load(self, source: Path):

        with open(source, 'r') as f:
            self.survey = json.load(f)
            self.source = source

    def validate(self) -> Union[OK, NOT_OK]:
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
                severity_scales_arr.append(SeverityScale(**{"name": item["type"],
                                                            "explanation": item["explanation"]}))

            survey_data = SurveyDataSchema(**{"severity_scales": severity_scales_arr,
                                              "survey_doc_id": survey_data["survey_doc_id"],
                                              "survey_type": survey_data["survey_type"],
                                              "survey_summary": survey_data["survey_summary"],
                                              "survey_purpose": survey_data["survey_purpose"]
                                              })

            self.valid_survey["survey_data"] = survey_data
            logger.info("Validating survey data. DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating vessel data {str(e)}")
            return NOT_OK

    def _validate_vessel_data(self) -> Union[OK, NOT_OK]:
        try:
            logger.info("Validating vessel_data...")
            vessel_data = self.survey["vessel_data"]

            survey_dimensions = vessel_data["dimensions"]
            dimensions: List[VesselDim] = []

            for item in survey_dimensions:

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

            self.valid_survey["vessel_data"] = vessel_data
            logger.info("Validating vessel_data.DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating vessel data {str(e)}")
            return NOT_OK

    def _validate_engine(self) -> Union[OK, NOT_OK]:

        try:
            logger.info("Validating engine...")
            vessel_data = self.survey["vessel_data"]
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

            self.valid_survey["vessel_engine"] = vessel_engine
            logger.info("Validating engine. DONE")
            return OK
        except Exception as e:
            logger.error(f"An error occurred whilst validating engine {str(e)}")
            return NOT_OK
