import socket
import asyncio
import sys


assert sys.platform == 'Linux', (
    'Cannot run the application on other than linux.'
)

MAYDAY = 1

SOCKET_FAMILY = socket.AF_INET
TYPE = socket.SOCK_RAW

PROTOCOL = {
    'TCP': socket.IPPROTO_TCP,
    'UDP': socket.IPPROTO_UDP,
    'ETHERNET': socket.ntohs(0x0003)
    }


class Connection:
    """
    Asynchronous socket raw streaming socket connection.
    : param protocol: tells the socket type of the protocol & which protocol connection packets should be sniffed.
    : type str : optional

    use:
       `async with Connection(protocol='UDP') as sock:
                sock.recv(2384)`
    Return as socket connection
    """
    def __init__(self, protocol=None, sock=None):
        self.protocol = PROTOCOL.get(protocol.upper(), None)
        if not self.protocol:
            self.protocol = PROTOCOL.get('TCP')   
        self.classname = type(self).__name__
        self.sock = sock if sock else socket.socket(SOCKET_FAMILY, TYPE, self.protocol)

    def __repr__(self):
        return f'{self.classname}(protocol={self.protocol})'

    async def __aenter__(self):
        try:
           return self.sock
        except socket.error as err:
            sys.stderr.write('Unable to make socket connection.{}'.format(err))
            sys.exit(MAYDAY)

    async def __aexit__(self, *args):
        if self.sock:
            self.sock.close()