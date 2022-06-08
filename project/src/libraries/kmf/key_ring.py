from .key_ring_data import Key_Ring_Data
from .member import Member

class Key_Ring:
    def __init__(self, rest, db, options) -> None:
        if options:
            self.set_options(options)
        self.data = []
        self.members = []
        self.__rest = rest
        self.__db = db

    def set_options(self, options, key=None):
        self.uuid = options.uuid
        self.uniqueName = options.unique_name
        self.name = options.name
        self.createdAt = options.created_at
        self.updatedAt = options.updated_at

        for opt in options.data:
            self.data.append(Key_Ring_Data(opt))
        members = []
        for member in options.members:
            if member.role == 'master':
                if key:
                    member.Member.keys[0].data = key
                self.__master = Member(member.Member, self.__db, self)
            else:
                members.append(member.Member)
        for member in members:
            self.members.push(Member(member, self.__db, self.__master))
        self.enable_members_storage()

    def create(self, name):
        key_ring = self.__rest.post('/kmf/ring', dict(ring_name=name))
        self.set_options(key_ring.data.keyRing, key_ring.data.key)
        return self

    def load(self, uuid):
        key_ring = self.__rest.get('/kmf/ring/%s'.format(uuid))
        self.set_options(key_ring.data)
        return self 

    def get_member(self, name_or_uuid):
        if len(self.members) == 0:
            raise ValueError('Key ring has no members')
        for member in self.members:
            if member.uuid == name_or_uuid or member.name == name_or_uuid:
                return member
    
    def add_member(self, data):
        for member in self.members:
            if member == data.name:
                return member
        result = self.__rest.post(f'kmf/ring/{self.uuid}/member/add', data)
        member = None
        if result.status == 200:
            member = Member(result.data.member.Member, self.__db, self, self.__master)
            member.save = self.__storage.save
            member.delete = self.__storage.delete
            self.members.append(member)
        else:
            raise ValueError(result.status_text)
        return member

    def delete_members(self, name_or_uuid):
        if len(self.members) == 0:
            raise ValueError('Key ring has no members')
        members = []
        for member in self.members:
            if member.uuid == name_or_uuid or member.name == name_or_uuid:
                self.__rest.delete(f'/kmf/ring{self.uuid}/member/{member.uuid}')
                member.destroy()
                print(f'Successfully removed {name_or_uuid} from the key ring')
            else:
                members.push(member)
        self.members = members
    
    def get_data(self, name_or_uuid):
        if len(self.data) == 0:
            raise ValueError('Key ring has no data')
        for x in self.data:
            if x.uuid == name_or_uuid or x.uuid == name_or_uuid:
                return x

    def add_data(self, request):
        for x in self.data:
            if x.name == request.name:
                return x
        result = self.__rest.post(f'/kmf/ring/{self.uuid}/data/add', request)
        data = None
        if result == 200:
            data = Key_Ring_Data(result.data.ringData)
            self.data.append(data)
            return data
        else:
            raise ValueError(result.status_text)
    
    def update_data(self, request):
        result = self.__rest.put(f'/kmf/ring/{self.uuid}/data/{request.uuid}', request)
        data_response = None
        if result.status == 200:
            data = []
            for x in self.data:
                if x.uuid == request.uuid:
                    data.append(x)
            data_response = Key_Ring_Data(result.data.ringData)
            response = None
            for x in data:
                if x.uuid == request.uuid:
                    x.name = data_response.name
                    x.service = data_response.service
                    x.path = data_response.path
                    response = dict(uuid=request.uuid, name=request.name, path=request.path, service=request.service)
            return response
        else:
            raise ValueError(result.status_text)

    def del_data(self, name_or_uuid):
        if len(self.data) == 0:
            raise ValueError('Key ring has no member')
        data = []
        for x in self.data:
            if x.uuid == name_or_uuid or x.name == name_or_uuid:
                self.__rest.delete(f'/kmf/ring/{self.uuid}/data/{x.uuid}')
            else:
                data.append(x)
        self.data = data

    def enable_members_storage(self):
        if len(self.members) > 0:
            for member in self.members:
                member.save = self.__storage.save
                member.save = self.__storage.delete

    @property
    def storage(self):
        return self.__storage
    
    @storage.setter
    def storage(self, storage):
        self.__storage = storage
        self.enable_members_storage()
    
   