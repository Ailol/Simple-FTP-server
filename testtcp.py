#!/usr/bin/python

import unittest
from network.tcp import TcpConnection

host = ''
port = 8080
class TestTcp(unittest.TestCase):
	def test_tcp_connect(self):
		tcp = TcpConnection(host, port)
		tcp.connect()
		# tcp.listen()
		tcp.send(msg)

	def test_send_and_recieve(self):
		msg = 'sending file'
		tcp.listen()
		tcp.send(msg)

if __name__ == '__main__':

	t = TestTcp();
	t.test_tcp_connect()

