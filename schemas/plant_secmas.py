from typing import List
from pydantic import BaseModel


class Plant(BaseModel):
    id: int
    plant_name: str
    science_name: str
    description: str

    class Config():
        orm_mode = True


class PlantMedicine(BaseModel):
    id: int
    medicene_type: str
    medicene_description: str

    class Config():
        orm_mode = True


class ShowDetails(BaseModel):
    id: int
    desease_name: str
    desease_short_description: str
    symptoms: str
    description: str
    belong_plant: Plant
    medicene: List[PlantMedicine]

    class Config():
        orm_mode = True
