#!/usr/bin/env python3
import sys
import threading
import socket
import logging


HOST = 'localhost' or '127.0.0.1'



class TCPConnection:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.host, self.port))
            return self.sock
        except Exception as sock_error:
            logging.error(sock_error)
            sys.exit(1)

    def __exit__(self):
        self.sock.close()



class TCP:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = int(sys.argv[1])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        print("Connected to ..", self.host, self.port)
        self.sock.listen(10)

    def proxy_handler(self, client_socket):
        request = client_socket.recv(1024)
        print(request)
        # Parse the url from the client request
        # the request url parsing method may varies
        first_line = request.split()
        url = first_line[1]
        url = url.decode('utf-8')
        url = url.replace('/', '')

        # Remote server socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((url, 80))
        s.sendall(request)
        while True:
            # Receive data, this must be a larger amount.
            data = s.recv(4096)
            if (len(data) > 0):
                client_socket.send(data)
            else:
                break

    def proxy(self):
        """Run the proxy server

        Usage:
            TCP().proxy()
        """
        while True:
            client_socket, addr = self.sock.accept()

            # You can use asyncio.
            proxy_thread = threading.Thread(target=self.proxy_handler,
                                            args=(client_socket,))
            proxy_thread.start()
