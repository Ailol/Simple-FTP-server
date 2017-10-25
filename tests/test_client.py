import unittest

from network.tcp import TcpConnection
from client import Client
from network.sftp import Sftp

host = ''
port = 8080

class TestClient(unittest.TestCase):
	def test_client_connect(self):
		client = Client(host, port)
		client.connect()
		client.request_server_content()
		client.request_file()

	# def test_client_decryption(self):

	# 	client = Client(host, port)
	# 	client.connect()
	# 	client.request_server_content()
	# 	client.download_file()
	# 	client.decrypt()

if __name__ == '__main__':

	c = TestClient();
	c.test_client_connect()

