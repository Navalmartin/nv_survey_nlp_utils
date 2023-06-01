from pydantic import BaseModel, Field, PositiveInt
from typing import List, Union


class SeverityScale(BaseModel):
    type: str = Field(title="type", alias="name")
    explanation: str = Field(title="explanation")


class SurveyDataSchema(BaseModel):
    survey_doc_id: str = Field(title="survey_doc_id")
    survey_type: str = Field(title="survey_type")
    survey_summary: str = Field(title="survey_summary")
    survey_purpose: str = Field(title="survey_purpose")
    severity_scales: Union[List[SeverityScale], None] = Field(title="severity_scales")
