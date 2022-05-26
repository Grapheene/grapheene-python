import jwt
import os
import src.libraries.rest.rest as rest


class TokenManager:
    def __init__(self, client_id, options):
        self.client_id = client_id
        self._proof = options.proof
        self._on_update = options.on_update
        self._auth_dir = options.auth_dir

        if not os.path.exists(self._auth_dir):
            os.path.makedirs(self._auth_dir)
        self._rest = rest.Rest() # TODO: figure out baseurl
        
    def auth(self, client_id, proof):
        if not proof or client_id:
            raise ValueError('Token manager is not set')
        # TODO figure out intervals and if need to clear 
        self.get_token()

    
    def get_auth(self, proof):
        return self.get_token(self.client_id, proof)
    
    def get_token(self, client_id, proof):
        try:
            result = self._rest.post('/auth', {'uuid': client_id, 'proof': proof})
            self._token = result.data['token']
            self._rsa = result.data['publicKey']

            token_path = self._auth_dir + os.path.sep + 'token'
            rsa_path = self._auth_dir + os.path.sep + 'rsa'

            with open(token_path, 'w') as f:
                f.write(self._token)
            
            with open(rsa_path, 'w') as f:
                f.write(self._rsa)
            
            self._on_update({'Token': self._token, 'Key': self._rsa})
            self.watch()
        except:
            raise ValueError('Unable to get Token')

    def load_token(self, client_id, proof):
        token_path = self._auth_dir + os.path.sep + 'token'
        rsa_path = self._auth_dir + os.path.sep + 'rsa'

        token = None
        rs = None

        if os.access(token_path, os.F_OK):
            token = open(token_path, 'r', encoding='utf8')
        
        if os.access(rsa_path, os.F_OK):
            rsa = open(rsa_path, 'r', encoding='utf8')

        valid = jwt.decode(token, rsa, algorithms=['RS256'])
    
    def watch(self): 
        pass