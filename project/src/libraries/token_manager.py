import jwt
import os
import datetime
import time
import asyncio
import codecs
import src.libraries.rest.rest as rest


class TokenManager:
    def __init__(self, client_id, rest_client, options):
        self.__client_id = client_id
        self.__proof = options.proof
        self.__on_update = options.on_update
        self.__auth_dir = options.auth_dir
        self.__event_loop = asyncio.new_event_loop()
        self.__delay = 60 if options.delay is None else options.delay

        if not os.path.exists(self._auth_dir):
            os.path.makedirs(self._auth_dir)
        self.__rest = rest_client
        
    def auth(self, client_id, proof):
        if not proof or client_id:
            raise ValueError('Token manager is not set')
        self.get_token()

    
    def get_auth(self, proof):
        return self.get_token(self.client_id, proof)
    
    def get_token(self, client_id, proof):
        try:
            result = self.__rest.post('/auth', {'uuid': client_id, 'proof': proof})
            self.__token = result.data['token']
            self.__rsa = result.data['publicKey']

            token_path = self.__auth_dir + os.path.sep + 'token'
            rsa_path = self.__auth_dir + os.path.sep + 'rsa'

            with open(token_path, 'w') as f:
                f.write(self._token)
            
            with open(rsa_path, 'w') as f:
                f.write(self._rsa)
            
            self.__on_update({'Token': self._token, 'Key': self._rsa})
            return result
           
        except:
            raise ValueError('Unable to get Token')

    def load_token(self, client_id, proof):
        # TODO: finish this function using verify
        token_path = self.__auth_dir + os.path.sep + 'token'
        rsa_path = self.__auth_dir + os.path.sep + 'rsa'

        token = None
        rs = None

        if os.access(token_path, os.F_OK):
            token = open(token_path, 'r', encoding='utf8')
        
        if os.access(rsa_path, os.F_OK):
            rsa = open(rsa_path, 'r', encoding='utf8')

   
    def verify_token(self, token, rsa_key):
        try:
            formated_key = codecs.decode(rsa_key, 'unicode_escape').strip('"')
            valid = jwt.decode(token, formated_key, algorithms=['RS256'])
        
            # get unix timestamp
            unix_time_stamp =time.mktime(datetime.datetime.now().timetuple())
            
            # check if within 300 seconds of expiring
            if valid['exp'] - unix_time_stamp <= 300:
                self.auth(self.__client_id, self.__proof)

        except jwt.ExpiredSignatureError as err:
            print ('Refreshing JWT...')
            self.auth(self.__client_id, self.__proof) 

        except Exception as err:
            print('Unable to refresh token')

    def watch_handler(self):
        self.verify_token(self.__token, self.__proof)
        self._timer_handle = None


    async def watch(self, delay): 
        if not self.__event_loop:
            raise ValueError('Event loop not initialized')
        if self._timer_handle is not None:
            return
        try:
            self._timer_handle = self.__event_loop.call_later(delay, self.watch_handler(self._token, self._proof))
        except:
            pass
        
    @property
    def jwt(self):
        return self.__token
    
    @property
    def public_key(self):
        return self.__rsa
    
    @property
    def proof(self):
        pass

    @proof.set
    def proof(self, proof):
        self.__proof = proof
