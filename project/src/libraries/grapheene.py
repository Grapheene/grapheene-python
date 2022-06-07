import os


class Grapheene:
    def __init__(self, client_id, api_key, token, opts=None) -> None:
        self.client_id = client_id
        self.api_key = api_key
        self.token = token
        self._options = opts

        self.files_dir = os.getcwd() + os.path.sep + self._options.project_dir + os.path.sep + self.client_id + os.path.sep + 'files'
        # TODO: initi path to orm directory here 


        self.zk_dir = self.files_dir + os.path.sep + 'zk'
        self.crypto_dir = self.files_dir + os.path.sep + 'encrypt'
        self.db_dir = self.files_dir + os.path.sep + 'db'
        self.auth_dir = self.files_dir + os.path.sep + 'auth'
    
    def __ensure_dir_exits(self):
        try:
            if not os.path.exists(self.zk_dir):
                os.makedirs(self.zk_dir)
            if not os.path.exists(self.crypto_dir):
                os.makedirs(self.crypto_dir)
            if not os.path.exists(self.db_dir):
                os.makedirs(self.db_dir)
            if not os.path.exists(self.auth_dir):
                os.makedirs(self.auth_dir)
        except:
            print("Error occured creating directories")

    def setup(self):
        try:
            self.__ensure_dir_exits()

            #TODO: setup orm session client

            #TODO: start writing out Zokrates

        except: 
            pass