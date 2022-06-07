from db import model
from json import dumps 

class Key:
    def __init__(self, options, db) -> None:
        self.uuid = options.uuid
        self.acitve = options.active
        self.created_at = options.created_at
        self.updated_at = options.updated_at
        self.__db = db

        if hasattr(options, 'data'):
            self.save(self.uuid, self.acitve, options.data)

    
    def save(self, uuid, active, key_data):
        try:
            if active == 'True':
                data = model.Key_Store(uuid=uuid, active=active, data=key_data)
                self.__db.create(data)
                self.__db.commit() 
                print('Successfully saved ${row.uuid} to the keyStore')
        except Exception as e:
            print(e)

    def load(self, type):
        try:
            key = self.__db.get(uuid=self.uuid)
            return dumps(key)
        except Exception as e:
            print(e)
            
    def destroy(self):
        try:
            self.__db.delete(uuid=self.uuid)
        except Exception as e:
            print(e)