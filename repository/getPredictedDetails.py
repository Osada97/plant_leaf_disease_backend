import models
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from env import Environment


def getPlantAllDetails(id: int, db: Session):
    plantDetails = db.query(models.PlantDesease).filter(
        models.PlantDesease.id == id).first()

    if plantDetails is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    if len(plantDetails.disease_image) > 0:
        for i in range(len(plantDetails.disease_image)):
            plantDetails.disease_image[i].image_name = f'{Environment.getBaseEnv()}assets/plant_disease_images/{plantDetails.disease_image[i].image_name}'

    else:
        plantDetails.default_image = f'{Environment.getBaseEnv()}defaults/communityDefault.jpg'

    return plantDetails
