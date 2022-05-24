import urllib3
import certifi

class Rest:
    def __init__(self, base_url) -> None:
        self.__http = urllib3.PoolManager(ca_certs=certifi.where())

    def delete(self, endpoint, params):
        return self.__http.request('DELETE', endpoint, fields=params, headers= dict({'Content-Type': 'application/json'}, **self.__headers))

    def download(self, endpoint, params=None):
        if not hasattr(params, 'path'):
            raise ValueError('Local path for downloading cloud data must be defined')
        #TODO get back to this one
        pass
    
    def get(self, endpoint, params=None):
        return self.__http.request('GET', endpoint, fields=params, headers= dict({'Content-Type': 'application/json'}, **self.__headers))

    def multipart_form(self, endpoint, params):
        pass

    def post(self, endpoint, data):
        return self.__http.request('POST', endpoint, body=data, headers= dict({'Content-Type': 'application/json'}, **self.__headers))

    def put(self, endpoint, data=None):
        return self.__http.request('PUT', endpoint, body=data, headers= dict({'Content-Type': 'application/json'}, **self.__headers))
        
    def set_headers(self, headers):
        self.__headers = headers