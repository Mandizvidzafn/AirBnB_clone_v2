from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import os
from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage:
    #private class attributes
    __engine = None
    __session = None

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
        if cls is not None:
            results = self.__session.query(cls).all()
            for obj in results:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                results = self.__session.query(cls).all()
                for obj in results:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects
    
    def new(self, obj):
        if obj:
            self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()