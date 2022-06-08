import keyring
from .key_ring import Key_Ring

class KMF:
    def __init__(self, rest, db):
        self.__rest = rest
        self.__db = db
        self.ring = Key_Ring(self.__rest, self.__db)
    
    def list(self):
        try:
            key_ring_res = self.__rest.get('/kmf/ring')
            if 200 <= key_ring_res.status < 300:
                return key_ring_res.data.keyRings
            
        except Exception as e:
            print(e)

    @property
    def ring(self):
        return self.__ring

    @ring.setter
    def ring(self, key_ring):
        self.__ring = key_ring

    def destroy(self):
        res = self.__rest.delete('/kmf/ring/', self.ring.uuid)
        self.ring = None
        return res