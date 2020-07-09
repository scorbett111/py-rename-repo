import os
import cryptography


class Auth:
    def __init__(self, config=None,):
  
        self.user = config.get(
            'user',
            os.getenv('REPO_USER')
        )
        self.password = config.get(
            'password',
            os.getenv('REPO_PASSWORD')
        )
        self.token = config.get(
            'token',
            os.getenv('REPO_TOKEN')
        )

        if self.token:
            self.type = 'token'
        else:
            self.type = 'password'

        self.encrypted = config.get('encrypted')


    def decrypt(self):
        fertnet = cryptography.fernet.Fernet(
            os.getenv('REPO_FERTNET_KEY')
        )

        if self.password:
            return fertnet.decrypt(self.password)
        elif self.token:
            return fertnet.decrypt(self.token)
        else:
            raise Exception('Error: No token or password to decrypt.')
        


        