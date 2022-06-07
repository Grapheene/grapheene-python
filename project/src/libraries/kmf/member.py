from os.path import sep
from .key import Key

class Member:
    __keys = []
    mode = None

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
        private_key, public_key = None
        
        try:
            private_key = self.__master.keys[0].load('private_key')
        except Exception as e:
            print('Unable to load master key:', e)
            raise e
        try:
            public_key = self.__keys[0].load('public_key')
        except: 
            print('Unable to load member key %s: %s'.format(self.__keys[0].uuid, e))
        return dict(private_key=private_key, public_key=public_key)
    
    def destroy(self):
        try:
            for key in self.__keys:
                key.destroy*()
        except Exception as e:
            raise e
    
    def data(self):
        self.__mode = 'data'
        return self
    
    def file(self):
        self.__mode = 'file'
        return self

    def encrypt(self, data_or_file_path, name=None):
        if not self.__mode:
            raise ValueError('encrypt must be used with file() or data()')
        if self.__mode != 'data':
            for index, key in enumerate(self.__key_ring.data):
                if key.path == data_or_file_path or key.data[index] == name:
                    return self.__key_ring.data[index]

        if self.__mode == 'data':
            if not name:
                raise ValueError('name is required for data mode')
            key_ring_data = dict(name=name, path='in:memory', encrypted='', service='unsaved')
            data = self.__key_ring.add_data(key_ring_data)
            ring_data = dict(data, **key_ring_data)
            self.__mode = None
            return ring_data

        if self.__mode == 'file':
            sp = data_or_file_path.split(sep)
            key_ring_data = dict(name= name if name else sp[-1], path=data_or_file_path, service='local')

            #add in encrypt function
            #encryption.encryptFile(data_or_file_path, self.__get_keys())
            data = self.__key_ring.add_data(key_ring_data)
            ring_data = dict(data, **key_ring_data)
            self.__mode = None
            return ring_data

    def decrypt(self, key_ring_data, path):
        if self.__mode:
            return self.decrypt_by_mode(key_ring_data)
        return self.decrypt_by_data_object(key_ring_data, path)

    def decrypt_by_data_object(self, key_ring_data, path):
        if key_ring_data.service == 'unsaved' and key_ring_data.path == 'in:memory':
            if not key_ring_data.encrypted:
                raise ValueError('encrypted is required for data mode, are you trying to decrypt and unencrypted object?')
            return dict(key_ring_data, decrypted=""" encryption.decrypt(key_ring_data.encrypted, self.__get_keys()) """)
        if key_ring_data.service == 'local':
            #add in encryption here
            #encryption.decrypt_file(key_ring_data.path, self.__get_keys())
            pass
        if key_ring_data.service == 'cloud' and key_ring_data.service == 'cloud:tmp:saved':
            if not path:
                raise ValueError('Set the path you would like to use for your temoporary storage')
            self.__key_ring.storage.get(key_ring_data, dict(path=path))
            #decrypt function
            #encryption.decrypt_file()
            key_ring_data = path
            key_ring_data.service = 'cloud:tmp:saved'
            return key_ring_data
    
    def decrypt_by_mode(self, key_ring_data):
        if not self.__mode:
            self.__mode = None
            raise ValueError('decrypt must be used with file() or data()')
        if self.__mode == 'data':
            if not key_ring_data.encrypted:
                raise ValueError('encrypted is required for data mode, are you trying to decrypt and unencrypted object?')
            self.__mode = None
            return dict(key_ring_data, decrypted=""" encryption.decrypt(key_ring_data.encrypted, self.__get_keys()) """)
        if self.__mode == 'file':
            """ encryption.decrypt(key_ring_data.encrypted, self.__get_keys()) """
            self.__mode = None
            return key_ring_data

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