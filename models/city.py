#!/usr/bin/python3
''' clase City que hereda de BaseModel '''

from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from models.place import Place
from models.state import State

class City(BaseModel):
    ''' Atributos de clase pública '''
    # Define ciudad para buscar
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    state = relationship("State", backref=backref("cities", cascade="all, delete"))
    places = relationship("Place", backref=backref("cities", cascade="all, delete"))
