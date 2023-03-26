#!/usr/bin/python3
''' Class FileStorage that serializes instances into a JSON file and
deserializes a JSON file into instances '''

import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


data = {"BaseModel": BaseModel, "User": User, "State": State,
        "Place": Place, "City": City, "Amenity": Amenity, "Review": Review}


class FileStorage:
    ''' Class that manages the storage of hbnb models
        in JSON format '''
    # string: path to JSON file
    __file_path = "file.json"
    # dictionary - empty
    __objects = {}

    def all(self, cls=None):
        ''' Returns the dictionary __objects '''
        if cls:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__:
                    new_dict[key] = value
            return new_dict
        return FileStorage.__objects

    def new(self, obj):
        ''' sets in __objects the obj with key <obj class name>.id '''
        # Stores all objects by <class name>.id
        # Ex. to store a BaseModel object with id = 12121212,
        # the key will be BaseModel.12121212
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        ''' Serializes __objects to the JSON file (path: __file_path) '''
        dic_obj = {}
        # Write operation:
        # Creates the JSON file where the serialized information will be stored
        with open(self.__file_path, "w", encoding="utf-8") as f:
            # Iterates over the entered values
            for key, value in self.__objects.items():
                # Assigns the value to dic_obj under its key
                dic_obj[key] = value.to_dict()
                # Converts Python objects into json objects suitable
                # for storage in a file
            json.dump(dic_obj, f)

    def reload(self):
        '''
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists; otherwise,
        if the file does not exist, no exception should be raised)
        '''
        try:
            # Read operation:
            # Opens the file for reading
            with open(self.__file_path, 'r', encoding='UTF-8') as f:
                # Deserializes the file
                j_dic = json.load(f)
            # Iterates over the contents of the deserialized file
            for key in j_dic:
                value = data[j_dic[key]["__class__"]](**j_dic[key])
                # Sets the object's new values
                self.__objects[key] = value
        # Raised when a requested file or directory does not exist
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

