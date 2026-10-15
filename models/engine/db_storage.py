#!/usr/bin/python3
"""
Contains the DBStorage class for database interaction using SQLAlchemy.
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Handles storage of models in a MySQL database using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database engine"""
        MYSQL_USER = getenv('HBNB_MYSQL_USER')
        MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        MYSQL_DB = getenv('HBNB_MYSQL_DB')
        ENV = getenv('HBNB_ENV')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB
            ),
            pool_pre_ping=True
        )

        if ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects of a given class"""
        obj_dict = {}
        classes = [State, City, User, Place, Amenity, Review]

        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            for c in classes:
                query = self.__session.query(c)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() on private session attribute (self.__session)"""
        self.__session.close()
