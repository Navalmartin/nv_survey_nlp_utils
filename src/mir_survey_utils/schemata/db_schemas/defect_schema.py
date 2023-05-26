import datetime
from datetime import datetime
from typing import Any, Optional, List, Union

import bson
from pydantic import BaseModel, Field, Extra

from navalmartin_mir_db_utils.utils.db_enums import InvalidTypeEnum


class DefectSchema(BaseModel):
    """defect mongodb document  schema"""

    idx: Optional[bson.ObjectId] = Field(title="idx",
                                         description="The MongoDB id associated with the document",
                                         alias="_id")

    vessel_type: str = Field(title="vessel_type",
                             description="The vessel type the defect was found",)

    defect_type: str = Field(
        title="defect_type",
        default=InvalidTypeEnum.INVALID.name.upper(),
        description="The descriptive type of the defect"
    )

    defect_labels: List[str] = Field(
        title="defect_labels",
        description="The textual description of the attached label",
        default=[InvalidTypeEnum.INVALID.name.upper()],
    )

    checkpoint_type: str = Field(
        title="checkpoint_type",
        description="The descriptive type of the checkpoint that the defect appears",
        default=InvalidTypeEnum.INVALID.name.upper(),
        alias="checkpoint_item"
    )

    survey_item_type: str = Field(
        title="survey_item_type",
        description="The descriptive type of the survey item that the checkpoint belongs",
        default=InvalidTypeEnum.INVALID.name.upper(),
        alias="checkpoint_group"
    )

    finding: str = Field(
        title="finding",
        description="The description of the finding",
        default=InvalidTypeEnum.INVALID.name.upper(),
    )

    finding_type: str = Field(
        title="finding_type",
        description="The descriptive type of the survey item that the checkpoint belongs",
        default=InvalidTypeEnum.INVALID.name.upper(),
    )

    severity_degree: str = Field(
        title="severity_degree",
        description="The severity degree of the defect",
        default=InvalidTypeEnum.INVALID.name.upper(),
        alias="severity"
    )

    recommendation_description: str = Field(title="recommendation_description",
                                            description="The recommendation associated with the defect",
                                            default=InvalidTypeEnum.INVALID.name.upper(),
                                            alias="recommendation")

    extra_recommendations_follow: Union[List[str], None] = Field(title="extra_recommendations_follow",
                                                                 description="Recommendations that can "
                                                                             "possibly follow the main recommendation",
                                                                 default=[InvalidTypeEnum.INVALID.name.upper()]
                                                                 )

    recommendation_choice_score: float = Field(title="recommendation_choice_score",
                                               description="The score that the recommendation associated "
                                                           "with this defect has been currently achieved",
                                               default=0.0)

    recommendation_choice_counter: int = Field(title="recommendation_choice_counter",
                                               description="How many times the recommendation "
                                                           "associated with this defect has been chosen",
                                               default=0)

    description: Union[str, None] = Field(title="description",
                                          description="Any extra description associated with the finding/defect",
                                          default=InvalidTypeEnum.INVALID.name.upper())

    comment_on_severity: Union[str, None] = Field(title="comment_on_severity",
                                                  description="Any extra description associated with the finding/defect",
                                                  default=InvalidTypeEnum.INVALID.name.upper(),
                                                  )

    created_at: Any = Field(
        title="created_at",
        description="Time and date the particular entry was created (UTC)",
        default=datetime.utcnow(),
    )
    updated_at: Any = Field(
        title="updated_at",
        description="Time and date the particular entry was updated (UTC)",
        default=datetime.utcnow(),
    )

    class Config:
        collection_name = "defects"
        orm_mode = True
        arbitrary_types_allowed = True
        indexes = ["_id", ]
        json_encoders = {
            bson.ObjectId: str,
        }
        extra = Extra.forbid
