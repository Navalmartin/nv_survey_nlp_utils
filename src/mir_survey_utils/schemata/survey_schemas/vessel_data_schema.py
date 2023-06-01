from pydantic import BaseModel, Field, PositiveInt
from typing import List, Union

from src.mir_survey_utils.schemata.survey_schemas.engine_data_schema import Engine


class VesselDim(BaseModel):
    name: str = Field(title="name")
    dimension: float = Field(title="dimension")
    metric: str = Field(title="metric")


class VesselDataSchema(BaseModel):
    vessel_name: str = Field(title="vessel_name")
    hull_material: str = Field(title="hull_material")
    hin: Union[str, None] = Field(title="hin")
    sea_category: Union[str, None] = Field(title="sea_category")
    vessel_type: str = Field(title="vessel_type")
    model_year: Union[str, None] = Field(title="model_year")
    survey_vessel_type: Union[str, None] = Field(title="survey_vessel_type")
    survey_vessel_model: Union[str, None] = Field(title="survey_vessel_model")
    ssr: Union[str, None] = Field(title="ssr")
    max_n_persons: Union[PositiveInt, None] = Field(title="max_n_persons")
    vessel_usage_type: str = Field(title="vessel_usage_type")
    dimensions: List[VesselDim] = Field(title="dimensions")
    engine: Engine = Field(title="engine")
