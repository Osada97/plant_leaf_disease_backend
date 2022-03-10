from fastapi import FastAPI
from routers import predictPlant
from routers.Community import admin, user, community
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
app.include_router(user.router)
app.include_router(community.router)
