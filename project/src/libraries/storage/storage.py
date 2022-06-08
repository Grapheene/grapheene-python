from os.path import exists, sep
from os import fstat, unlink, makedirs


class Storage:
    def __init__(self, options, rest, kmf):
        self.__rest = rest
        self.__kmf = kmf
        self.__medium = options.medium
    
    def local(self):
        self.__medium = 'local'
        return self
    
    def cloud(self):
        self.__medium = 'cloud'
        return self
    
    def find(self, file_name):
        for x in self.__kmf.ring.data:
            if x.name == file_name:
                return x
        return None
    
    def list(self):
        return self.__kmf.ring.data

    def save(self, key_ring_data, options=None):
        if options and options.name:
            key_ring_data.name = options.name
        origin_path = key_ring_data.path
        try:
            if not self.__medium:
                raise ValueError('local() or cloud() medium must be selected')
            
            if self.__medium == 'local' and key_ring_data.path == 'in:memory':
                if not options or not options.path:
                    raise ValueError('Filepath is required for data')
                sp = options.path.split(sep)
                if not options or not options.path:
                    member = self.__kmf.ring.members[0]
                    data = member.decrypt(key_ring_data)
                    self.saveLocal(options.path, sp[-1], data.decrypted)
                    member.file().encrypt(options.path)
                return self.__kmf.ring.update_data(dict(uuid=key_ring_data.uuid, path=options.path, name=sp[-1], service=self.__medium))
            
            if self.__medium == 'local' and origin_path != 'in:memory':
                path = None
                if key_ring_data.service == 'cloud':
                    path = self.get(key_ring_data, dict(path=options.path))
                    self.delete_cloud(key_ring_data.path)
                    
                return self.__kmf.ring.update_data(dict(uuid=key_ring_data.uuid, path=options.path, name=sp[-1], service=self.__medium))
            
            if self.__medium == 'cloud':
                if origin_path == 'in:memory':
                    sp = options.path.split(sep)
                    member = self.__kmf.ring.members[0]
                    key_ring_data.path = origin_path
                    data = member.decrypt(key_ring_data)
                    self.save_loca(options.path, sp[-1], data.decrypted)
                    key_ring_data = member.file().encrypt(options.path)
                    key_ring_data.service = 'local'
                cloud_data = self.save_cloud(key_ring_data)
                return self.__kmf.ring.update_data(dict(uuid=key_ring_data.uuid, path=cloud_data.id, name=sp[-1], service=self.__medium))
            
            self.__medium = None
        except Exception as e:
            self.__medium = None
            print(f'Unable to save keyring data:{e}')
            raise e
    
    def delete(self, ring_data):
        try:
            self.__kmf.ring.del_data(ring_data.uuid)
            
            if ring_data.service == 'local':
                self.delete_local(ring_data.path, ring_data.name)
            
            if ring_data.service == 'cloud':
                self.delete_cloud(ring_data.uuid)
            return True
        except Exception as e:
            raise e

    def download(self, ring_data, options):
        try:
            if not hasattr(options, 'path'):
                raise ValueError('Local path for downloading cloud data must be defined')
            name = options.name if options.name else ring_data.name
            file_path = options.path
            saved_path = self.__rest.download(f'/file/{ring_data.uuid}', dict(path=file_path))
            return self.__kmf.ring.update_data(dict(uuid=ring_data.uuid, path=saved_path, name=name, service='local'))
        except Exception as e:
            raise e
    
    def get(self, ring_data, options):
        try:
            if not hasattr(options, 'path'):
                raise ValueError('Local path for downloading cloud data must be defined')
            file_path = options.path
            saved_path = self.__rest.download(f'/file/{ring_data.uuid}', dict(path=file_path))
            return saved_path
        except Exception as e:
            raise e
    
    def save_local(self, file_path, file_name, data):
        try:
            file = file_path.replace(sep + file_name, '')
            with open(file + sep + file_name, 'w', encoding='utf-8') as f:
                f.write(data)
            return True
        except Exception as e:
            raise e

    def save_cloud(self, key_ring_data):
        try:
            save_path = key_ring_data.path
            stats = fstat(save_path)
            params = dict(file=save_path, size=stats.count)
            result = self.__rest.multi_part_form('/upload', params)
            unlink(save_path)
            return result.data
        except Exception as e:
            raise e

    def delete_cloud(self, file_id):
        try:
            self.__rest.delete(f'/file/{file_id}')
        except Exception as e:
            raise e
    
    def delete_local(self, file_path, file_name):
        try:
            unlink(file_path + sep + file_name)
            return True
        except Exception as e:
            raise e

    def create_dir(self, file_path):
        if not exists(file_path):
            makedirs(file_path)
    
    def load(self, file_id):
        return self

    @property
    def kmf(self):
        return self.__kmf

    @kmf.setter
    def kmf(self, kmf):
        self.__kmf = kmf