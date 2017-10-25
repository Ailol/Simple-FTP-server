import argparse
import os

from network.sftp import Sftp


class Server(object):

    """
        Simple server implementation
        SFTP holds all the magic

        Starts the server up by arguments given by the user.
    """

    def __init__(self, *args):
        try:
            self.sftp = Sftp(args[0], args[1])
        except BaseException:
            raise ValueError('hepp')

    def connect(self):
        self.sftp.setup_connection()

    def list_content(self):
        for file in os.listdir("./server_disk"):
            print(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A simple way to transfer encrypted files')
    parser.add_argument(
        'host',
        type=str,
        help='Enter host (example: localhost)',
        default='localhost')
    parser.add_argument(
        'port',
        type=int,
        help='Enter port(8000->)',
        default=8080)

    args = parser.parse_args()

    srv = Server(args.host, args.port)
    srv.connect()
