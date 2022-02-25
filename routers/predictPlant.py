from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from repository.getPredictedDetails import getPlantAllDetails
from repository.predictPlant import predictImage
from schemas import plant_secmas


router = APIRouter()

# prediction of the plant


@router.post('/predict',  tags=['predict-plant'])
async def predict(db: Session = Depends(get_db), file: UploadFile = File(..., media_type='image/jpeg'), model: str = 'potato'):
    return await predictImage(db, file, model)

# get plant details


@router.get('/getplantdetails/{id}', response_model=plant_secmas.ShowDetails, tags=['predict-plant'])
def getPlantPredictedDetails(id: int, db: Session = Depends(get_db)):
    return getPlantAllDetails(id, db)

# **plant details section**

# get disease
# get plant
# get medicine

# update disease
# update plant
# update medicine

# **plant images**

# add plant image
# remove specific plant image
# update plant image
