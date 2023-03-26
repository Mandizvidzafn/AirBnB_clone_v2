#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from models import storage

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    #class attributes
    id = Column(String(60), unique=True, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                if k != "__class__":
                    setattr(self, k, v)
            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())
            time = datetime.utcnow()
            if "created_at" not in kwargs.keys():
                self.created_at = time
            if "updated_at" not in kwargs.keys():
                self.updated_at = time
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()


    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        #from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""

        dictionary = self.__dict__.copy()
        if "_sa_instance_state" in dictionary:
            dictionary.pop('_sa_instance_state', None)
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary['__class__'] = type(self).__name__
        return dictionary
    
    def delete(self):
        """Delete the current instance from the storage"""

        #from models import storage
        storage.delete(self)
