from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from repository.getPredictedDetails import getPlantAllDetails
from repository.plantDetails import getDiseaseOnId, getMedicineOnId, getPlantOnId, updateDetails, updateDisease, updateMedicine
from repository.predictPlant import predictImage
from schemas import plant_secmas


router = APIRouter()

# prediction of the plant


@router.post('/predict',  tags=['predict plant'])
async def predict(db: Session = Depends(get_db), file: UploadFile = File(..., media_type='image/jpeg'), model: str = 'potato'):
    return await predictImage(db, file, model)

# get plant details


@router.get('/getplantdetails/{id}', response_model=plant_secmas.ShowDetails, tags=['predict plant'])
def getPlantPredictedDetails(id: int, db: Session = Depends(get_db)):
    return getPlantAllDetails(id, db)

# **plant details section**

# get plant based on id


@router.get('/getdetails/plant/{id}', response_model=plant_secmas.Plant, tags=['CRUD plant'])
def getPlantDetails(id: int, db: Session = Depends(get_db)):
    return getPlantOnId(id, db)

# get disease based on id


@router.get('/getdetails/disease/{id}', response_model=plant_secmas.Disease, tags=['CRUD plant'])
def getPlantDiseaseDetails(id: int, db: Session = Depends(get_db)):
    return getDiseaseOnId(id, db)

# get medicine based on id


@router.get('/getdetails/medicine/{id}', response_model=plant_secmas.PlantMedicine, tags=['CRUD plant'])
def getPlantMedicineDetails(id: int, db: Session = Depends(get_db)):
    return getMedicineOnId(id, db)

# update disease based on id


@router.put('/updatedetails/disease/{id}', response_model=plant_secmas.PlantDiseaseUpdate, tags=['CRUD plant'])
def updatePlantMedicineDetails(request: plant_secmas.PlantDiseaseUpdate, id: int, db: Session = Depends(get_db)):
    return updateDisease(request, id, db)

# update plant based on id


@router.put('/updatedetails/details/{id}', response_model=plant_secmas.PlantUpdate, tags=['CRUD plant'])
def updatePlantDetails(request: plant_secmas.PlantUpdate, id: int, db: Session = Depends(get_db)):
    return updateDetails(request, id, db)
# update medicine based on id


@router.put('/updatedetails/medicine/{id}', response_model=plant_secmas.PlantMedicineUpdate, tags=['CRUD plant'])
def updatePlantMedicineDetails(request: plant_secmas.PlantMedicineUpdate, id: int, db: Session = Depends(get_db)):
    return updateMedicine(request, id, db)

# **plant images**

# add plant image
# remove specific plant image
# update plant image
