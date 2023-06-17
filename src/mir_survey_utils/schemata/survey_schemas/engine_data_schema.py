from pydantic import BaseModel, Field, PositiveInt
from typing import List, Union


class EngineEntry(BaseModel):
    engine_manufacturer: Union[str, None] = Field(title="engine_manufacturer",
                                                  description="The manufacturer of the engine")

    engine_model: Union[str, None] = Field(title="engine_model",
                                           description="The engine model")

    engine_size: Union[float, None] = Field(title="engine_size",
                                            description="The size of the engine")

    engine_size_metric: Union[str, None] = Field(title="engine_size_metric",
                                                 description="The metric unit used to measure the engine size")

    engine_type: Union[str, None] = Field(title="engine_type",
                                          description="The type of the engine")

    hp: Union[int, None] = Field(title="hp",
                                 default=1,
                                 description="The horse power of the engine",
                                 ge=1)

    engine_hours: Union[float, None] = Field(title="engine_hours",
                                             default=0.0,
                                             description="The total hours of operation of the engine",
                                             ge=0.0)

    build_date: Union[str, None] = Field(title="build_date",
                                         description="The build date of the  engine")


class Engine(BaseModel):
    number_of_engines: int = Field(
        title="number_of_engines",
        description="The total number of engines"
    )
    engines: List[EngineEntry] = Field(title="engines")
