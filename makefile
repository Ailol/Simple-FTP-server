all: clean-pyc clean-build run

clean:clean-pyc clean-build

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

autopep:
	autopep8 --in-place --aggressive --aggressive server.py
	autopep8 --in-place --aggressive --aggressive client.py
	autopep8 --in-place --aggressive --aggressive ./network/sftp.py
	autopep8 --in-place --aggressive --aggressive ./network/tcp.py
	autopep8 --in-place --aggressive --aggressive ./utils/encrypt.py
test:
	python3 test_tcp.py
	python3 test_server.py

test_client:
	python3 test_client.py