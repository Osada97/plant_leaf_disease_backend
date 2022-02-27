from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models


def getPlantAllDetails(id: int, db: Session):
    plantDetails = db.query(models.PlantDesease).filter(
        models.PlantDesease.id == id).first()

    if plantDetails is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    return plantDetails
