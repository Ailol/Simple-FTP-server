import argparse, os
import socket as sock
from server import Server
from network.sftp import Sftp
from network.tcp import TcpConnection as tcp
from utils.encrypt import CryptoGenerator as CG
from Crypto.PublicKey import RSA



class Client(object):
    """
        Main client, sends a RSA publickey to gain access and a request for a file.
        If granted access after checking for RSA key, the file recived is
        decrypted by the original private key, and decrypted to plaintext.

    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = sock.socket()
        self.server = Server(host, port)
        self.run()
    
    def run(self):
        self.connect()
        self.request_server_content()
        self.request_file()


    def connect(self):
        self.socket.connect((self.host, self.port)) 

    def request_server_content(self):
        """
            Lists current server content
        """
        self.server.list_content()

    def request_file(self):
        """
            First sends request that generates RSA for permission.
            Then if accepted, recieve_file decrypts the data and writes to client disk.

        """
        self.send_request() 
        self.recieve_file()

    def send_request(self):

        """
            generate_rsa returns a tuple(privatekey, publickey)
            Generates RSA and sends publickey.
   
        """

        self.filename = input('what do you want to retrieve?: ')
        self.rsa = CG.generate_rsa()
        self.socket.sendall(self.filename.encode('utf-8') + self.rsa[1].exportKey())

    def recieve_file(self):

        """
            Checks if server found or granted access. 
            If nothing is recieved, it defaults to None, 
            else decrypts and writes to file.
        """

        self.socket.settimeout(1)
        try:
            key = self.rsa[0].decrypt(self.socket.recv(256))
        except:
            key = None
            data = None
            print('Nothing recieved, did you write the correct filename?')
        if key is not None:
            data = CG.decrypt_aes256(self.socket.recv(4096).decode('utf-8'), key)
            self.write_file(data)

    def write_file(self, data):
        """ 
            Writes the recieved content into a new file. 

            @param data: decrypted ciphertext
        """
        file = open('./client_disk/new_'+self.filename, 'wb')
        file.write(data)
        file.close()
        print('downloaded!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client side of Simple secure ftp server.')
    parser.add_argument('host', type=str, help='Enter host (example: localhost)', default='localhost')
    parser.add_argument('port', type=int, help='Enter port(8000->)', default=8080)

    args = parser.parse_args()
    cl = Client(args.host, args.port)
 
