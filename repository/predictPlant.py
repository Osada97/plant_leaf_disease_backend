import os
import cv2
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
from pathlib import Path
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
import models

# load models
MODEL = tf.keras.models.load_model("./Model/Potato/2")  # potato train model
PAPPERMODEL = tf.keras.models.load_model(
    "./Model/Papper/1.h5")  # papper train model

# model classes
CLASS_NAMES = [{'name': 'Early blight', 'id': 0}, {
    'name': "Late Blight", 'id': 1}, {'name': "Healthy", 'id': 2}]
PAPPER_CLASS_NAMES = [
    {'name': 'Pepper bell bacterial spot', 'id': 3}, {'name': 'Pepper bell healthy', 'id': 4}]


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

# resize image


def resizeImage(image):
    # CLAHE
    # hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # h,s,v = hsv_img[:,:,0],hsv_img[:,:,1],hsv_img[:,:,2]
    # clahe = cv2.createCLAHE(clipLimit=1.0,tileGridSize=(2,2))
    # v = clahe.apply(v)
    # hsv_img = np.dstack((h,s,v))

    # resize_image
    imgResize = cv2.resize(image, (256, 256))

    # remove noise smoothing
    imgResize = cv2.medianBlur(imgResize, 3)

    return imgResize

# save image
# convert list as image and save


def list_as_a_image(data, fileName, model, className):
    Path(
        f"./assets/usersImages/{model}/{className['name']}").mkdir(parents=True, exist_ok=True)
    img = np.array(data).astype(np.uint8)
    data = Image.fromarray(img)
    data.save(f"./assets/usersImages/{model}/{className['name']}/{fileName}")
    return

 # function for get data base details about plant details plant disease details and medicine details


def getPlantDetails(db: Session):
    return db.query(models.Plant).all()


async def predictImage(db: Session, file, model):

    # check file type
    if file.content_type not in ["image/jpeg", "image/jpeg"]:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'{file.content_type} is invalid file type please upload jpeg files.')

    image = read_file_as_image(await file.read())

    # openCV function
    AfterCVImage = resizeImage(image)

    img_batch = np.expand_dims(AfterCVImage, 0)

    if model == 'potato':
        predictions = MODEL.predict(img_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    elif model == 'pepper':
        predictions = PAPPERMODEL.predict(img_batch)
        predicted_class = PAPPER_CLASS_NAMES[np.argmax(predictions[0])]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{model} query string not found')

    confidence = np.max(predictions[0])

    # save user upload files
    list_as_a_image(AfterCVImage, file.filename, model, predicted_class)

    # get data base details about plant details plant disease details and medicine details
    details = getPlantDetails(db)

    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }
