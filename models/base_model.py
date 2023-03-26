#!/usr/bin/python3
''' Class BaseModel '''

import models
from datetime import datetime
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

Base = declarative_base()


class BaseModel:
    
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    '''
    Base class that defines all the
    common attributes/methods for other classes
    '''
    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            # Iterate through the key and value in the items entered
            for key, value in kwargs.items():
                # Assign the key to the current creation date
                if key == "created_at":
                    self.created_at = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                # Assign the key to the updated date
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                # Assign the value to the key
                # self: Object whose attribute is to be assigned.
                # key: Object attribute to be assigned.
                # value: Value with which the variable will be assigned.
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            # Assign random id
            self.id = str(uuid.uuid4())
            # Assign current date
            self.created_at = datetime.now()
            # Update last modification date
            self.updated_at = self.created_at
            # If it is a new instance
            # not from a dictionary representation
            

    def __str__(self):
        ''' returns the name of the class, ID and
        the attribute dictionary '''
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        ''' updates the public instance attribute
        updated_at with the current date and time '''
        self.updated_at = datetime.now()
        # call the storage save(self) method
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        ''' returns a dictionary containing all
        keys/values of __dict__ of the instance '''
        dic = self.__dict__.copy()
        dic["created_at"] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        dic["updated_at"] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        dic["__class__"] = self.__class__.__name__
        # Remove _sa_instance_state key if exists
        dic.pop('_sa_instance_state', None)
        return dic

    def delete(self):
        ''' deletes the current instance from storage '''
        models.storage.delete(self)
