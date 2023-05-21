from pydantic import BaseModel, Field


class SurveyItemDataSchema(BaseModel):
    survey_item: str = Field(title="survey_item")
    severity: str = Field(title="severity")
    comment_on_severity: str = Field(title="comment_on_severity")
    survey_item_synopsis: str = Field(title="survey_item_synopsis")