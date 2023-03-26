#!/usr/bin/python3
''' Clase FileStorage que serializa instancias en un archivo JSON y
deserializa un archivo JSON en instancias '''
''' Class FileStorage that serializes instances into a JSON file and
deserializes a JSON file into instances '''

import json
from models.base_model import BaseModel
from models.state import State
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

data = {"BaseModel": BaseModel, "User": User, "State": State,
        "Place": Place, "City": City, "Amenity": Amenity, "Review": Review}


class FileStorage:
    ''' Clase que gestiona el almacenamiento de modelos
        hbnb en formato JSON '''
    # cadena: ruta al archivo JSON
    ''' Class that manages the storage of hbnb models
        in JSON format '''
    # string: path to JSON file
    __file_path = "file.json"
    # diccionario - vacío
    # dictionary - empty
    __objects = {}

    def all(self):
        ''' Devuelve el diccionario __objects '''
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
        ''' establece en __objects el obj con la clave <obj class name>.id '''
        # Almacenará todos los objetos por <nombre de clase>.id
        # Ej. Para almacenar un objeto BaseModel con id = 12121212,
        # la clave será BaseModel.12121212
        ''' sets in __objects the obj with key <obj class name>.id '''
        # Stores all objects by <class name>.id
        # Ex. to store a BaseModel object with id = 12121212,
        # the key will be BaseModel.12121212
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        ''' Serializa __objects en el archivo JSON (ruta: __file_path) '''
        ''' Serializes __objects to the JSON file (path: __file_path) '''
        dic_obj = {}
        # Operación de escritura:
        # Creo el archivo json donde se almacenara la información a serializar
        # Write operation:
        # Creates the JSON file where the serialized information will be stored
        with open(self.__file_path, "w", encoding="utf-8") as f:
            # Recorro los valores ingresados
            # Iterates over the entered values
            for key, value in self.__objects.items():
                # Asigno el valor al dic_obj en su clave
                # Assigns the value to dic_obj under its key
                dic_obj[key] = value.to_dict()
                # Convierte los objetos de Python en objetos json apropiados
                # para almacenarse en un archivo
                # Converts Python objects into json objects suitable
                # for storage in a file
            json.dump(dic_obj, f)

    def reload(self):
        '''
        Deserializa el archivo JSON a __objects
        (solo si el archivo JSON (__file_path) existe; de ​​lo contrario,
        si el archivo no existe, no se debe generar ninguna excepción)
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists; otherwise,
        if the file does not exist, no exception should be raised)
        '''
        try:
            # Operación de lectura:
            # Se abre el archivo para lectura
            # Read operation:
            # Opens the file for reading
            with open(self.__file_path, 'r', encoding='UTF-8') as f:
                # Se deserializa el archivo
                # Deserializes the file
                j_dic = json.load(f)
            # Se recorre el contenido del archivo deserializado
            # Iterates over the contents of the deserialized file
            for key in j_dic:
                value = data[j_dic[key]["__class__"]](**j_dic[key])
                # Establece los nuevos valores del objeto
                value = data[j_dic[key]["__class__"]](**j_dic[key])
                # Sets the object's new values
                self.__objects[key] = value
        # Se genera cuando se solicita un archivo o directorio pero no existe
        # Raised when a requested file or directory does not exist
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
