import socket
import asyncio
import sys


assert sys.platform == 'Linux', (
    'Cannot run the application on other than linux.'
)

MAYDAY = 1

# sniffing only TCP packets.
SOCKET_FAMILY = socket.AF_INET
TYPE = socket.SOCK_RAW

PROTOCOL = {
    'TCP': socket.IPPROTO_TCP,
    'UDP': socket.IPPROTO_UDP,
    'ETHERNET': socket.ntohs(0x0003)
    }


class Connection:

    def __init__(self, protocol=None):
        self.protocol = PROTOCOL.get(protocol.upper(), None)
        if not self.protocol:
            self.protocol = PROTOCOL.get('UDP')   
        self.classname = type(self).__name__
    
    def __repr__(self):
        return f'{self.classname}(protocol={self.protocol})'

    def __aenter__(self):
        try:
            self.sock = socket.socket(SOCKET_FAMILY, TYPE, self.protocol)
            return self.sock
        except socket.error as err:
            sys.stderr.write('Unable to make socket connection.{}'.format(err))
            sys.exit(MAYDAY)

    def __aexit__(self, *args):
        self.sock.close()