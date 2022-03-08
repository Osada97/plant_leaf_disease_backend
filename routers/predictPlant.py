from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user
from repository.diseaseImage import addPlantToDesease, removeDiseaseImage
from repository.getPredictedDetails import getPlantAllDetails
from repository.plantDetails import getDiseaseOnId, getMedicineOnId, getPlantOnId, updateDetails, updateDisease, updateMedicine
from repository.predictPlant import predictImage
from schemas import plant_secmas, admin_schemas


router = APIRouter()

# prediction of the plant


@router.post('/predict',  tags=['predict plant'])
async def predict(file: UploadFile = File(..., media_type='image/jpeg'), model: str = 'potato'):
    return await predictImage(file, model)

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
def getPlantMedicineDetails(id: int, db: Session = Depends(get_db), current_user: admin_schemas.Login = Depends(get_current_user)):
    return getMedicineOnId(id, db)

# update disease based on id


@router.put('/updatedetails/disease/{id}', response_model=plant_secmas.PlantDiseaseUpdate, tags=['CRUD plant'])
def updatePlantMedicineDetails(request: plant_secmas.PlantDiseaseUpdate, id: int, db: Session = Depends(get_db), current_user: admin_schemas.Login = Depends(get_current_user)):
    return updateDisease(request, id, db)

# update plant based on id


@router.put('/updatedetails/details/{id}', response_model=plant_secmas.PlantUpdate, tags=['CRUD plant'])
def updatePlantDetails(request: plant_secmas.PlantUpdate, id: int, db: Session = Depends(get_db), current_user: admin_schemas.Login = Depends(get_current_user)):
    return updateDetails(request, id, db)
# update medicine based on id


@router.put('/updatedetails/medicine/{id}', response_model=plant_secmas.PlantMedicineUpdate, tags=['CRUD plant'])
def updatePlantMedicineDetails(request: plant_secmas.PlantMedicineUpdate, id: int, db: Session = Depends(get_db), current_user: admin_schemas.Login = Depends(get_current_user)):
    return updateMedicine(request, id, db)

# **plant disease images**

# add plant image


@router.post('/disease/addimage/{id}', tags=['Disease image'])
def addImageDisease(id: int, db: Session = Depends(get_db), file: UploadFile = File(..., media_type='image/jpeg'), current_user: admin_schemas.Login = Depends(get_current_user)):
    return addPlantToDesease(id, db, file)


# remove specific plant image using plant id
@router.delete('/disease/removeimage/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Disease image'])
def removeImageById(id: int, db: Session = Depends(get_db), current_user: admin_schemas.Login = Depends(get_current_user)):
    return removeDiseaseImage(id, db)
