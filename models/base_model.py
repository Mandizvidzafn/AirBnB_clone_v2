#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    #class attributes
    id = Column(String(60), unique=True, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel"""

        if not kwargs.get('id'):
            self.id = str(uuid.uuid4())
        else:
            self.id = kwargs['id']

        self.created_at = kwargs['created_at'] = datetime.utcnow() \
            if 'created_at' not in kwargs else kwargs['created_at']
        self.updated_at = kwargs['updated_at'] = datetime.utcnow() \
            if 'updated_at' not in kwargs else kwargs['updated_at']

        for key, value in kwargs.items():
            setattr(self, key, value)


    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""

        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state', None)
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary['__class__'] = type(self).__name__
        return dictionary
    
    def delete(self):
        """Delete the current instance from the storage"""

        from models import storage
        storage.delete(self)
