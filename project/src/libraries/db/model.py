from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Key_Store(Base):
    __tablename__ = 'keyStore'
    uuid = Column(String, primary_key=True)
    active  = Column(Boolean)
    data = Column(String)

    def __init__(self, uuid, active, data) -> None:
        super().__init__(self)

    def to_json(self):
        return dict(uuid=self.uuid, active=self.active, data=self.data)

    def __repr__(self) -> str:
        return "<Key(uuid='%s', active='%s', data='%s')>" % (self.uuid, self.active, self.data)

    @property
    def is_active(self):
        return self.active
    
    @property 
    def get_data(self):
        return self.data 