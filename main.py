from fastapi import FastAPI
from routers import predictPlant
from routers.Community import admin
import models
from database import engine

app = FastAPI()

# data base
models.Base.metadata.create_all(engine)


@app.get("/ping")
def ping():
    return "Hello,I am Live"


app.include_router(predictPlant.router)
app.include_router(admin.router)
