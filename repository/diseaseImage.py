from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import shutil
import os
import time
import models

# **disease image section**
# add plant to disease


def addPlantToDesease(id: int, db: Session, file):
   # check file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'{file.content_type} is invalid file type please upload jpeg and png files.')

    path = './assets/plant_disease_images'
    # check specific file directory exits
    isExist = os.path.exists(path)

    if not isExist:
        # create new directory
        os.makedirs(path)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    filenames = timestr+file.filename
    file_location = f'{path}/{filenames}'
    with open(file_location, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_image = models.PlantDiseaseImages(image_name=filenames, disease_id=id)
    try:
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return new_image
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} is not in the disease table please check the id and try again')


def removeDiseaseImage(id: int, db: Session):
    # get the specific file name
    plant_image = db.query(models.PlantDiseaseImages).filter(
        models.PlantDiseaseImages.id == id).first()

    if plant_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} is not in the disease image table please check the id and try again')

    path = './assets/plant_disease_images'
    if os.path.exists(path):
        file_location = path + '/'+plant_image.image_name
        if os.path.exists(file_location):
            # remove the file from server
            os.remove(file_location)
            # remove row in the table
            db.query(models.PlantDiseaseImages).filter(
                models.PlantDiseaseImages.id == id).delete(synchronize_session=False)
            db.commit()
            return {'detail': f'{id} image deleted'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{plant_image.image_name} is not in the server')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no image in the server')
