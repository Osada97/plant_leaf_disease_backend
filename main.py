from fastapi import FastAPI
from routers import predictPlant
from routers.Community import admin, user, community
import models
from database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:19002/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# data base
models.Base.metadata.create_all(engine)

app.mount("/defaults", StaticFiles(directory="defaults"), name="defaults")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get("/ping")
def ping():
    return "Hello,I am Live"


app.include_router(predictPlant.router)
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(community.router)
