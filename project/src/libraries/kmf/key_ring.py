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
    
   