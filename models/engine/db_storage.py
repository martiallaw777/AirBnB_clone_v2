#!/usr/bin/python3
"""This module defines a class to manage db  storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """This class manages storage of hbnb models in database"""
    __engine = None
    __session = None

    def __init__(self):
        """ initialize storage """
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB")), pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ print all data """
        if not cls:
            result = self.__session.query(State).all()
            result.extend(self.__session.query(City).all())
            result.extend(self.__session.query(User).all())
            result.extend(self.__session.query(Place).all())
            result.extend(self.__session.query(Review).all())
            result.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            result = self.__session.query(cls).all()
        result = {
                f"{type(obj).__name__}.{obj.id}":
                obj.to_dict() for obj in result}
        return result

    def new(self, obj):
        """ add new object to session"""
        self.__session.add(obj)

    def save(self):
        """ save session to database """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete object """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reload from db """
        Base.metadata.create_all(self.__engine)
        session_ = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_)()
