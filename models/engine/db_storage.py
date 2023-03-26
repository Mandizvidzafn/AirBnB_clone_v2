from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
import os


class DBStorage:
    __engine = None
    __session = None
    __classes = {"BaseModel": BaseModel, "User": User, "State": State,
                 "Place": Place, "City": City, "Amenity": Amenity, "Review": Review}

    def __init__(self):
        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        database = os.environ.get('HBNB_MYSQL_DB')
        env = os.environ.get('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, database),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        objects = {}
        if cls is None:
            for key, value in self.__classes.items():
                if key != "BaseModel":
                    objs = self.__session.query(value).all()
                    for obj in objs:
                        k = obj.__class__.__name__ + "." + obj.id
                        objects[k] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                k = obj.__class__.__name__ + "." + obj.id
                objects[k] = obj

        return objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

