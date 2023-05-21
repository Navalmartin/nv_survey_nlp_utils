from pydantic import BaseModel, Field
from typing import Union


class CheckpointDataSchema(BaseModel):
    checkpoint_item: str = Field(title="checkpoint_item")
    checkpoint_group: Union[str, None] = Field(title="checkpoint_group")
    comment_on_severity: str = Field(title="comment_on_severity")
    synopsis: str = Field(title="synopsis")
    severity: str = Field(title="severity")
