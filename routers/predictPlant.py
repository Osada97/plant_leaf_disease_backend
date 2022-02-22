from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from repository.predictPlant import predictImage


router = APIRouter()

# prediction of the plant


@router.post('/predict', tags=['predict-plant'])
async def predict(db: Session = Depends(get_db), file: UploadFile = File(..., media_type='image/jpeg'), model: str = 'potato'):
    return await predictImage(db, file, model)
