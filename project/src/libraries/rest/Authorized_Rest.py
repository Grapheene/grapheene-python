from os import access, F_OK
from os.path import exists
from rest import Rest
from jwt import decode, ExpiredSignatureError
from time import mktime
from datetime import datetime
from warnings import warn
from json import dumps
from codecs import decode as c_decode

class AuthorizedRest(Rest):
    __auth_dir = None
    TOKEN_PATH = "{dir}/token".format(dir=__auth_dir)
    KEY_PATH = "{dir}/rsa".format(dir=__auth_dir)

    def __init__(self, base_url, client_id, auth_dir, zk) -> None:
        super().__init__(base_url)
        self.__base_url = base_url
        self.__client_id = client_id
        self.__auth_dir = auth_dir
        self.zk = zk

    def __get_auth_files(self):

        token = None
        key = None

        if exists(self.TOKEN_PATH) and access(self.TOKEN_PATH, F_OK):
            token = open(self.TOKEN_PATH)
        else:
            return False

        if exists(self.KEY_PATH) and access(self.KEY_PATH, F_OK):
            key = open(self.KEY_PATH)
        else:
            return False

        return dict(Token=token, Key=key)

    def initialize(self):
        try:
            files = self.__get_auth_files()
            if files:
                self.__update_rest_headers(dict(Token=files.Token, Key=files.Key))

                valid = self.is_jwt_valid()
                if valid == 'warn' or not valid:
                    self.__refresh_jwt()
                    return True
                
                return True
            print('Auth files do not exist updating Auth')
            self.__refresh_jwt

        except:
            self.__refresh_jwt()

    def is_jwt_valid(self):
        try:
            files = self.__get_auth_files()
            valid = decode(files.Token, files.Key)
            
            # get current unix timestamp
            unix_time_stamp = mktime(datetime.now().timetuple())

            # check if within 300 seconds of expiring
            if (valid['exp'] - unix_time_stamp) <= 300:
                warn('JWT will expire soon, we will refresh soon.')
                return 'warn'
            
            return True

        except ExpiredSignatureError as err:
            print ('Refreshing JWT...')
            self.__refresh_jwt()
            return True 

        except Exception as err:
            print('Unable to refresh token')
            return False

    def auth(self, endpoint, params):
        print('Getting new JWT')
        return super().post(endpoint=endpoint, data=params)
        
    def __refresh_jwt(self,):
        try:
            # TODO when zk is done
            result = self.auth('/auth', dict(uuid=self.__client_id, proof= dumps(self.zk.generateProof())))
            self.__token, = self.result.data['token']
            self.__key = c_decode(self.result.data['key'], 'unicode_escape').strip('"')

            # write token and key to files
            with open(self.TOKEN_PATH, 'w') as f:
                f.write(self.__token)

            with open(self.KEY_PATH, 'w') as f:
                f.write(self.__key)

            response = dict(Token=self.__token, Key=self.__key)
            self.__update_rest_headers(response)
            return response

        except Exception as e:
            print(e)
            raise e

    def __update_rest_headers(self, headers):
        super().set_headers(headers)
