# Simple-FTP-server

## A simple encryption transfer for files
	Implemented by using pycrypto libraries, and AES/RSA hybrid.
	Symmetric keys are used to encrypt data, and asymmetric for
	handshaking. This is due to optimizing performance as asymmetric
	is expensive for large data. 

## Running the file
	positional arguments:
	  host        Enter host (example: localhost)
	  port        Enter port(8000->)

	python server.py host port
	python client.py host port

##Makefile
Used mainly for formatting, cleanup and tests.



