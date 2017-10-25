# from encryption.encrypt import encrypt_aes256, decrypt_aes264
from . tcp import TcpConnection
import threading
import os

from utils.encrypt import CryptoGenerator as CG
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64encode
from base64 import b64decode
from Crypto import Random


"""
chr() server side, ord() on client side.

chr takes in ascii values and returns a char
that corresponds.

ORD reveres it, and return a ASCII value of a character. 


"""
ERRORMSG = 'FILENOTFOUND'
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

class Sftp(TcpConnection):

    """
        Recieves request from client, which then checks for publickey.
        Grants access if present, and servers the requested file.
        The file is encrypted with AES before send over the wire. 

    """

    def __init__(self, host, port):
        super(Sftp, self).__init__(host, port)
        self.host = host
        self.port = port
        self.CG = CG()

    def setup_connection(self):
        self.connect()
        self.listen()

    def listen(self):
        """
            Polls continuously for clients and data. 

            Connected clients need to send RSA publickey and a file request 
            inorder to gain access to the server.
        """


        while True:
            self.client, address = self.socket.accept()
            print(('CONNECTED: @ ' + str(address))) 

            try:
                ciphertext = self.request_handler(self.client.recv(4096).decode('utf-8'))  
                self.client.sendall(ciphertext[0])
                self.client.sendall(ciphertext[1])     
                print('file uploaded, awaiting next client')         
            except ValueError:
                pass
            print(('DISCONNECTED:  @ ' + str(address))) 
        self.socket.close()
  

    def request_handler(self, data):
        """
            Checks for correct keys, and routes to either the server disk, or 
            denies access. 
        """


        if self.check_permission(data) != -1:
            return self.upload_file(data)
        else:
            self.denied_access()

    def check_permission(self, data):
        """ 
            @Returns -1 if not found
        """

        return data.find("-----BEGIN PUBLIC KEY-----")

    def denied_access(self):
        """
            If publickey is not found, raises valuerror
        """

        raise ValueError('You not permitted to enter the area of this server, \n did you remember to bring the publickey?')
    
    def upload_file(self, data):
        """
            Main encryption function

            sends data and publickey to encrypt generator. If the requested file
            does not exists, a valueerror is raised. 
            Encrypt_aes256 recieves content and raw data.

            @Returns a tuple(generated rsa, b64encode(cipherblock))


        """

        return CG.encrypt_aes256(self.get_file(data), self.CG.check_publickey(data))

    def get_file(self, data):
        """
            Serves the file upwards, first checks if the file exists, and 
            if found, creates a filepath. Then reads and returns red content. 

            @return content of file
        """

        filepath = self.check_if_exists(data)
        file = open(filepath, 'rb')
        content = file.read()
        file.close()
        return content

    def check_if_exists(self, data):
        """
            Checks the server for requested file.

            @Returns filepath if found, else nothing is sendt. 
        """

        for file in os.listdir("./server_disk"):
            if data.find(file) != -1:
                return self.create_filepath(file)
        
        raise ValueError('File does not exist! Returning...')    

    def create_filepath(self, data):
        """
            Creates a complete filepath to requested file
            @Returns string to filepath
        """

        filepath = '{}/{}'.format(os.getcwd(), 'server_disk/')
        if os.path.isdir(filepath):
            return filepath + data


