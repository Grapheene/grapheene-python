import uuid


from .key import Key

class Member:
    __keys = []
    
    def __init__(self, options, db, key_ring, master=None) -> None:
        self.uuid = options.uuid
        self.name = options.name
        self.__key_ring = key_ring
        self.__db = db
        if master:
            self.__master = master
        self.unique_name = options.uuid + ':' + options.uuid
        for key in options.keys:
            self.__keys.insert(Key(key, self.__db))

    def __get_keys(self):
        try:
            pass
        except:
            pass
    
    def destroy(self):
        pass
    
    def data(self):
        pass
    
    def file(self):
        pass

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def decrypt_by_data(self, ):
        pass
    
    def decrypt_by_mode(self):
        pass

    @property
    def  keys(self):
        return self.__keys

    @property
    def save(self):
        return self.__save

    @property
    def delete(self):
        return self.__delete

    @save.setter
    def save(self, save):
        self.__save = save

    @delete.setter
    def delete(self, delete):
        self.__delete = delete