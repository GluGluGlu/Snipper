import paramiko
from io import StringIO
import os


class BaseAuthentication:
    """Base class for SSH authentication."""

    def authenticate(self, hostname, port, ssh_client):
        raise NotImplementedError("Subclasses must implement this method")


class UsernamePasswordAuthentication(BaseAuthentication):
    """Authentication using username and password."""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, hostname, port, ssh_client):
        ssh_client.connect(hostname=hostname, port=port, username=self.username, password=self.password)


class UsernamePrivateKeyAuthentication(BaseAuthentication):
    """Authentication using username and private key."""

    def __init__(self, username, private_key, key_type=None):
        self.username = username
        self.private_key = private_key
        self.key_type = key_type

    def load_private_key(self):
        """Load private key from file path or key string."""
        if isinstance(self.private_key, str):
            if os.path.isfile(self.private_key):
                with open(self.private_key, 'r') as key_file:
                    key_data = key_file.read()
                if not self.key_type:
                    self.key_type = detect_key_type(key_data)
                    # print(f"Detected {self.key_type} Key Type")
            else:
                key_data = self.private_key

            if self.key_type == 'RSA':
                return paramiko.RSAKey.from_private_key(file_obj=StringIO(key_data))
            elif self.key_type == 'ECDSA':
                return paramiko.ECDSAKey.from_private_key(file_obj=StringIO(key_data))
            elif self.key_type == 'Ed25519':
                return paramiko.Ed25519Key.from_private_key(file_obj=StringIO(key_data))
            else:
                raise ValueError("Unsupported key type")
        else:
            raise ValueError("Private key must be a file path or a key string")

    def authenticate(self, hostname, port, ssh_client):
        pkey = self.load_private_key()
        ssh_client.connect(hostname=hostname, port=port, username=self.username, pkey=pkey)


def detect_key_type(key_data):
    """Detect the type of the private key based on its header."""
    if key_data.startswith('-----BEGIN RSA PRIVATE KEY-----'):
        return 'RSA'
    elif key_data.startswith('-----BEGIN EC PRIVATE KEY-----'):
        return 'ECDSA'
    elif key_data.startswith('-----BEGIN OPENSSH PRIVATE KEY-----'):
        return 'RSA'
    else:
        raise ValueError("Unsupported key type or unknown key format")