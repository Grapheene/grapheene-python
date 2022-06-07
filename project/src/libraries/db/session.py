from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Session:
    def __init__(self, db_connect_string, Base, Model):
        # create db engine
        self.__engine = create_engine(db_connect_string)
        
        # creating localized session object 
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        # attaching the base for top level use. 
        self.__base = Base
        self.__model = Model

    def commit(self):
        self.__session.commit()
        
    def setupDB(self):
        self.__base.metadata.create_all(self.__engine)

    def get(self, uuid=None):
        if uuid:
            return self.__session.query(self.__model).one(uuid=uuid)
        return self.__session.query(self.__model).all()
    
    def create(self, data):
        if not data:
            raise ValueError('data is missing')
        return self.__session.add(data)
        
    def delete(self, uuid):
        key = self.get(uuid=uuid)
        return self.__session.delete(key)
    