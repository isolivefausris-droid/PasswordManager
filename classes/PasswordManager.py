import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import keyring

class PasswordManager:
    def __init__(self, master_password: str): 
        self.salt = None
        self.passwords = {}
        self.path = '../psw/container.json'
        if os.path.exists(self.path):
            self._load()
        else:
            self.salt = os.urandom(16)
            self._save()
        self.key = self._derive_key(master_password)
        self.cipher = Fernet(self.key)
    def _derive_key(self, password: str) -> bytes:
        kdf =  PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=600_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    def add_password(self, login: str, password: str):
        encrypted_password = self.cipher.encrypt(password.encode())
        self.passwords[login] = encrypted_password.decode()
        self._save()
    def get_password(self, login: str):
        encrypted_password =  self.passwords[login]
        decrypted_password = self.cipher.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    def list_services(self):
        return list(self.passwords.keys())
    def delete_pswd(self, login: str):
        del self.passwords[login]
        self._save()
    def _save(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            data = {'salt':base64.urlsafe_b64encode(self.salt).decode(), 'passwords':self.passwords}
            json.dump(data, file)
    def _load(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.salt = base64.urlsafe_b64decode(data['salt'].encode())
            self.passwords = data.get('passwords', {})
