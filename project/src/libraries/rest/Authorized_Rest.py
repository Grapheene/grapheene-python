import rest
import token_manager
import json

class Authorized_Rest(rest.Rest):
    def __init__(self, base_url, client_id, rest_client, zk, auth_dir):
        super().__init__(base_url)
        self.token_manager = token_manager.TokenManager(client_id, rest_client, options={
            "proof": json.dumps(zk.generateProof(), separators=(',', ':')),
            "auth_dir": auth_dir,
            "on_update": self.update_rest_headers
        })
        self.update_rest_headers({"Token": self.token_manager.jwt, "Key": json.dumps(self.token_manager.public_key)})

    def update_rest_headers(self, headers):
        super().set_headers(headers)
    
    
    def ensure_headers(self):
        if not hasattr(self.__http.headers, "Token") or not hasattr(self.__http.headers("Key")):
            try:
                result = self.token_manager.get_auth(json.dumps(self.zk.generate_proof()))
                self.update_rest_headers({"Token": result.data.token, "key": json.dumps(result.data.public_key)})
            except Exception as e:
                raise e
    
    # REST Crud Wrappers
    def get(self, endpoint, params):
        self.ensure_headers()
        return super().get(endpoint, params)
    
    def post(self, endpoint, params):
        self.ensure_headers()
        return super().post(endpoint, params)
    
    def put(self, endpoint, params):
        self.ensure_headers()
        return super().put(endpoint, params)
    
    def delete(self, endpoint, params):
        self.ensure_headers()
        return super().delete(endpoint, params)