from typing import List, Optional
from pydantic import BaseModel, Field

# details of the plant


class Plant(BaseModel):
    id: int
    plant_name: str
    science_name: str
    description: Optional[str] = None

    class Config():
        orm_mode = True

# details of the plant Medicine


class PlantMedicine(BaseModel):
    id: int
    medicene_type: str
    medicene_description: Optional[str] = None

    class Config():
        orm_mode = True

# details of the plant medicine and disease (relationship)


class DiseaseImages(BaseModel):
    id: int
    image_name: str

    class Config():
        orm_mode = True


class ShowDetails(BaseModel):
    id: int
    desease_name: str
    desease_short_description: str
    disease_image: List[DiseaseImages] = []
    default_image: Optional[str] = None
    symptoms: Optional[str] = None
    description: Optional[str] = None
    belong_plant: Plant
    medicene: List[PlantMedicine] = []

    class Config():
        orm_mode = True

# details of the plant disease


class Disease(BaseModel):
    id: int
    desease_name: str
    desease_short_description: str
    symptoms: Optional[str] = None
    description: Optional[str] = None

    class Config():
        orm_mode = True


# update plant
class PlantUpdate(BaseModel):
    science_name: str = Field(..., min_length=1, max_length=155)
    description: str

    class Config():
        orm_mode = True

# update disease


class PlantDiseaseUpdate(BaseModel):
    desease_name: str = Field(..., min_length=1,  max_length=155)
    desease_short_description: str = Field(..., min_length=1, max_length=155)
    symptoms: Optional[str] = None
    description: Optional[str] = None

    class Config():
        orm_mode = True


class PlantMedicineUpdate(BaseModel):
    medicene_type: str = Field(..., min_length=1,  max_length=155)
    medicene_description: Optional[str] = None

    class Config():
        orm_mode = True
