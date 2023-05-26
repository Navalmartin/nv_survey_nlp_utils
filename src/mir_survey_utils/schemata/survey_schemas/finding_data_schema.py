from pydantic import BaseModel, Field, PositiveInt
from typing import List, Union


class FindingDataSchema(BaseModel):
    id: Union[str, int] = Field(title="id")
    finding_type: str = Field(title="finding_type")
    checkpoint_item: str = Field(title="checkpoint_item")
    checkpoint_group: Union[str, None] = Field(title="checkpoint_group")
    finding: str = Field(title="finding")
    defect_labels: Union[List[str], None] = Field(title="defect_labels")
    recommendation: str = Field(title="recommendation")
    extra_recommendations_follow: Union[List[str], None] = Field(title="extra_recommendations_follow")
    description: Union[str, None] = Field(title="description")
    severity: str = Field(title="severity")
    comment_on_severity: Union[str, None] = Field(title="comment_on_severity")
