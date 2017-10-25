from .exceptions import BadDataException
import base64
from base64 import b64decode, b64encode
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

RSAKEY = 2048
BLOCK_SIZE = 16  # Bytes


def pad(s): return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s): return s[:-ord(s[len(s) - 1:])]


class CryptoGenerator(object):

    """
        A cryptographic layer that encrypts and decrypts data using symmetric keys.
        Also generates a asymmetric key for identification purposes upon connection.

    """

    def __init__(self):
        self.init = None

    def generate_rsa():
        """
            Creates a fres RSA key, returns a tuple of
            (Privatekey, Publickey)
        """

        print('GENERATING RSAKEY')
        rsa = RSA.generate(RSAKEY, Random.new().read)
        publickey = rsa.publickey()
        return (rsa, publickey)

    def get_key(self, data):
        """
            Slices the private key from strings
        """

        return data[data.find("-----BEGIN PUBLIC KEY-----")
                              :data.find("-----END PUBLIC KEY-----") + 26]

    def check_publickey(self, data):
        """
            Checks for RSA key, either publig or private half.
            Accepts recieved data from client, no need to manipulate beforehand.

            Returns RSA key
        """

        return RSA.importKey(self.get_key(data))

    def decrypt_aes256(cipher, key):
        """
            Decrypts recieved ciphertext and turns it into plaintext.
        """

        return unpad(AES.new(key[16:], AES.MODE_CBC,
                             key[:16]).decrypt(b64decode(cipher)))

    def encrypt_aes256(data, rsa):
        """

        """
        iv = Random.new().read(AES.block_size)
        key = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        keyz = rsa.encrypt(iv + key, '')[0]  # Otherwise turned into tuple
        return (keyz, b64encode(iv + cipher.encrypt(pad(data.decode('utf-8')))))
