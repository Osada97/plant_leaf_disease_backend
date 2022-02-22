from sqlalchemy import Column, ForeignKey, Integer, String, Text
from database import Base
from sqlalchemy.orm import relationship

# main three tables for prediction (plant details, plant disease details and disease medicine table)


class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String(155), nullable=False)
    science_name = Column(String(155), nullable=False)
    description = Column(Text)

    disease = relationship(
        "PlantDesease",  back_populates='belong_plant')


class PlantDesease(Base):
    __tablename__ = 'plant_deseases'

    id = Column(Integer, primary_key=True, index=True)
    desease_name = Column(String(155), nullable=False)
    desease_short_description = Column(String(155), nullable=True)
    symptoms = Column(Text, nullable=True)
    description = Column(Text)
    plant_id = Column(Integer, ForeignKey(
        'plants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    belong_plant = relationship(
        'Plant',  back_populates='disease')
    medicene = relationship("PlantDeseaseMedicene",
                            back_populates="plant_medicene")
    disease_image = relationship("PlantDiseaseImages",
                                 back_populates="plant_image")


class PlantDeseaseMedicene(Base):
    __tablename__ = "plant_desease_medicines"

    id = Column(Integer, primary_key=True, index=True)
    medicene_type = Column(String(155), nullable=False)
    medicene_description = Column(Text, nullable=False)
    disease_id = Column(Integer, ForeignKey(
        'plant_deseases.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)

    plant_medicene = relationship('PlantDesease', back_populates='medicene')

# plant_disease image model use for add images for plant diseases


class PlantDiseaseImages(Base):
    __tablename__ = "plant_disease_images"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(Text)
    disease_id = Column(Integer, ForeignKey(
        'plant_deseases.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)

    plant_image = relationship(
        'PlantDesease', back_populates='disease_image')
