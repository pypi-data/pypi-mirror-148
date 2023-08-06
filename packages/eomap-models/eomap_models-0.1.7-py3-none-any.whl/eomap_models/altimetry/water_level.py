from pydantic import BaseModel, Field
from datetime import datetime


class WaterLevelObservation(BaseModel):
    lon: float = Field(..., title="Longitude")
    lat: float = Field(..., title="Latitude")
    date: datetime
    waterlevel: float = Field(alias="waterlevel_ocog")
    elevation: float = Field(alias="elevation_ocog")
    geoid_height: float
    orbit: int
    sigma_0_ocog: float

    class Config:
        allow_population_by_field_name = True