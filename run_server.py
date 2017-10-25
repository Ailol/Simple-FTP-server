import unittest
from network.sftp import Sftp
from server import Server


host = ''
port = 8080

class TestSftp(unittest.TestCase):
	def test_sftp_connect(self):
		server = Server(host, port)
		server.connect()


if __name__ == '__main__':

	t = TestSftp();
	t.test_sftp_connect()

