import urllib3
import certifi
import json

class Rest:
    def __init__(self, base_url) -> None:
        self.__http = urllib3.PoolManager(ca_certs=certifi.where())
        self.url = base_url

    
    def delete(self, endpoint, params):
        self.__http.headers['Content-Type'] = 'application/json'
        return self.__http.request('DELETE', self.url + endpoint, fields=params)

    
    def download(self, endpoint, params=None):
        if not hasattr(params, 'path'):
            raise ValueError('Local path for downloading cloud data must be defined')
        #TODO get back to this one
        pass
    
   
    def get(self, endpoint, params=None):
        self.__http.headers['Content-Type'] = 'application/json'
        return self.__http.request('GET', self.url + endpoint, fields=params)

   
    def multipart_form(self, endpoint, params):
        pass

   
    def post(self, endpoint, data):
        self.__http.headers['Content-Type'] = 'application/json'
        endcoded_data = json.dumps(data)
        return self.__http.request('POST', self.url + endpoint, body=endcoded_data)

   
    def put(self, endpoint, data=None):
        self.__http.headers['Content-Type'] = 'application/json'
        endcoded_data = json.dumps(data)
        return self.__http.request('PUT', self.url + endpoint, body=endcoded_data)
        
    def set_headers(self, headers):
        self.__http.headers = headers