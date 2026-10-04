#!/usr/bin/python3

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


class DBStorage:
    """Database storage engine."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage."""
        user = os.getenv("HBNB_MYSQL_USER", "hbnb_dev")
        password = os.getenv("HBNB_MYSQL_PWD", "hbnb_dev_pwd")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        database = os.getenv("HBNB_MYSQL_DB", "hbnb_dev_db")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                user,
                password,
                host,
                database
            ),
            pool_pre_ping=True
        )

    def all(self, cls=None):
        """Query all objects in the current database session."""
        objects = {}

        classes = {
            "User": User,
            "State": State,
            "City": City,
            "Place": Place,
            "Review": Review
        }

        if cls is not None:
            if isinstance(cls, str):
                cls = classes.get(cls)

            if cls is None:
                return objects

            classes = {
                cls.__name__: cls
            }

        for class_obj in classes.values():
            for obj in self.__session.query(class_obj).all():
                key = "{}.{}".format(
                    obj.__class__.__name__,
                    obj.id
                )
                objects[key] = obj

        return objects

    def new(self, obj):
        """Add an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and initialize the database session."""
        BaseModel.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )

        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current database session."""
        self.__session.remove()
