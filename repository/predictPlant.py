import os
import cv2
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
from pathlib import Path

# load models
MODEL = tf.keras.models.load_model("./Model/Potato/2")  # potato train model
PAPPERMODEL = tf.keras.models.load_model(
    "./Model/Papper/1.h5")  # papper train model

# model classes
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
PAPPER_CLASS_NAMES = [
    "Pepper bell bacterial spot", "Pepper bell healthy"]


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
        f"./assets/usersImages/{model}{className}").mkdir(parents=True, exist_ok=True)
    img = np.array(data).astype(np.uint8)
    data = Image.fromarray(img)
    data.save(f"./assets/usersImages/{model}{className}/{fileName}")
    return


async def predictImage(file, model):

    image = read_file_as_image(await file.read())

    # openCV function
    AfterCVImage = resizeImage(image)

    img_batch = np.expand_dims(AfterCVImage, 0)

    if model == 'potato':
        predictions = MODEL.predict(img_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    elif model == 'papper':
        predictions = PAPPERMODEL.predict(img_batch)
        predicted_class = PAPPER_CLASS_NAMES[np.argmax(predictions[0])]

    confidence = np.max(predictions[0])

    # save user upload files
    list_as_a_image(AfterCVImage, file.filename, 'potato', predicted_class)

    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }
