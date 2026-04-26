import keyring
import os
import base64 
class AuthManager:
    def __init__(self):
        self.username = os.getlogin()
        self.service = "MyPSWDServ"
    def _get_pswd(self):
        pswd = keyring.get_password(self.service, self.username)
        if pswd:
            return pswd 
        keyring.set_password(self.service, self.username, base64.urlsafe_b64encode(os.urandom(32)).decode() )
        return keyring.get_password(self.service, self.username)
