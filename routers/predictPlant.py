from fastapi import APIRouter, UploadFile, File

from repository.predictPlant import predictImage


router = APIRouter()


@router.post('/predict', tags=['predict-plant'])
async def predict(file: UploadFile = File(..., media_type='image/jpeg'), model: str = 'potato'):
    return await predictImage(file, model)
