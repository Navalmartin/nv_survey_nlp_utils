from pathlib import Path
from typing import Union, Any
import json
from .condition_survey_validator_pimpl import ConditionSurveyValidatorPimpl

OK = "OK"
NOT_OK = "NOT_OK"


class ConditionSurveyValidator(object):

    def __init__(self, survey_json_doc: Path = None, validate: bool = False):

        self.pimpl = ConditionSurveyValidatorPimpl(survey_json_doc=survey_json_doc,
                                                   validate=validate)

    def __getitem__(self, item) -> Any:
        return self.valid_survey[item]

    @property
    def is_valid(self) -> bool:
        return self.pimpl.is_valid

    @property
    def survey(self) -> dict:
        return self.pimpl.survey

    @property
    def source(self) -> Path:
        return self.pimpl.source

    @property
    def filename(self) -> str:
        return self.source.name

    @property
    def valid_survey(self) -> dict:

        if not self.is_valid:
            raise ValueError("The survey data is not valid")

        return self.pimpl.valid_survey

    def load(self, source: Path) -> None:
        self.pimpl._load(source=source)

    def validate(self) -> Union[OK, NOT_OK]:
        return self.pimpl._validate()

    def save(self, filename: Path) -> None:
        if filename.suffix != '.json':
            raise ValueError("json format is expected here.")

        with open(filename, 'w') as f:
            json.dump(self.valid_survey, f, indent=1)
