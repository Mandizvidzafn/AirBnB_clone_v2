#!/usr/bin/python3
''' clase State que hereda de BaseModel '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.city import City
from . import storage


class State(BaseModel, Base):
    ''' Atributos de clase pública '''
    # clase para crear un estado
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    

    @property
    def cities(self):
        """ Getter attribute that returns the list of City instances
        with state_id equals to the current State.id """
        city_instances = storage.all(City)
        return [city for city in city_instances.values() if city.state_id == self.id]


