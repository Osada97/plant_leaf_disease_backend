from sqlalchemy import Column, ForeignKey, Integer, String, Text
from database import Base
from sqlalchemy.orm import relationship


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


class PlantDeseaseMedicene(Base):
    __tablename__ = "plant_desease_medicines"

    id = Column(Integer, primary_key=True, index=True)
    medicene_type = Column(String(155), nullable=False)
    medicene_description = Column(Text, nullable=False)
    desease_id = Column(Integer, ForeignKey(
        'plant_deseases.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    plant_medicene = relationship('plant_deseases', back_populates='medicene')
