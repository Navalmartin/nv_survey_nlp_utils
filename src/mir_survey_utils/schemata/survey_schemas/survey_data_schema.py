from pydantic import BaseModel, Field, PositiveInt
from typing import List, Union


class SeverityScale(BaseModel):
    type: str = Field(title="type", alias="name")
    explanation: str = Field(title="explanation")


class SurveyDataSchema(BaseModel):
    survey_doc_id: str = Field(title="survey_doc_id")
    survey_type: str = Field(title="survey_type")
    survey_summary: Union[str, None] = Field(title="survey_summary")
    survey_purpose: Union[str, None] = Field(title="survey_purpose")
    severity_scales: Union[List[SeverityScale], None] = Field(title="severity_scales")
    estimated_vessel_value: Union[float, None] = Field(title="estimated_vessel_value",
                                                       description="The estimated overall evaluation of "
                                                                   "the vessel according to the survey")
    currency_of_estimation: Union[str, None] = Field(title="currency_of_estimation",
                                                     description="The currency used to report the "
                                                                 "estimated overall evaluation of "
                                                                 "the vessel according to the survey")
