from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import plant_secmas
import models


def getDiseaseOnId(id: int, db: Session):
    plantDisease = db.query(models.PlantDesease).filter(
        models.PlantDesease.id == id).first()

    if plantDisease is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    return plantDisease


def getPlantOnId(id: int, db: Session):
    plantDetails = db.query(models.Plant).filter(models.Plant.id == id).first()

    if plantDetails is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    return plantDetails


def getMedicineOnId(id: int, db: Session):
    plantMedicineDetails = db.query(models.PlantDeseaseMedicene).filter(
        models.PlantDeseaseMedicene.id == id).first()

    if plantMedicineDetails is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    return plantMedicineDetails


def updateDisease(request: plant_secmas.PlantDiseaseUpdate, id: int, db: Session):
    plant_disease = db.query(models.PlantDesease).filter(
        models.PlantDesease.id == id).first()

    if plant_disease is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    plant_disease.desease_name = request.desease_name
    plant_disease.desease_short_description = request.desease_short_description
    plant_disease.symptoms = request.symptoms
    plant_disease.description = request.description

    db.commit()
    db.refresh(plant_disease)

    return plant_disease


def updateMedicine(request: plant_secmas.PlantDiseaseUpdate, id: int, db: Session):
    plant_medicine = db.query(models.PlantDeseaseMedicene).filter(
        models.PlantDeseaseMedicene.id == id).first()

    if plant_medicine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    plant_medicine.medicene_type = request.medicene_type
    plant_medicine.medicene_description = request.medicene_description

    db.commit()
    db.refresh(plant_medicine)

    return plant_medicine


def updateDetails(request: plant_secmas.PlantUpdate, id: int, db: Session):
    plant_details = db.query(models.Plant).filter(
        models.Plant.id == id).first()

    if plant_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Id is invalid')

    plant_details.science_name = request.science_name
    plant_details.description = request.description

    db.commit()
    db.refresh(plant_details)

    return plant_details
