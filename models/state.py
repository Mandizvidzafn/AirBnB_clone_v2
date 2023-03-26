#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref 
import models


class State(BaseModel, Base):
    """
    State class inherits from BaseModel and Base
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if models.storage_t == "db":
        cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        """
        Getter attribute that returns the list of City instances with state_id
        equals to the current State.id
        """
        from models.city import City
        city_list = []
        for city in models.storage.all(City).values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
