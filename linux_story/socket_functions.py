# socket_functions.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Create server so terminal and GUI can communicate with each other


import json
import socket
import SocketServer


server_busy = None


def is_server_busy():
    return server_busy


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self, arg1, arg2, arg3):
        self.continue_server = True
        SocketServer.BaseRequestHandler.__init__(self, arg1, arg2, arg3)

    def handle(self):

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(4096).strip()
        print self.data
        data_dict = json.loads(self.data)
        self.server.queue.put(data_dict)


def create_server(queue):
    HOST, PORT = "localhost", 9959

    # Create the server, binding to localhost on port 9999

    # Magic line that allows you to reuse the address, even if a
    # different server is using it.  This means if we launch this and then
    # quit it, we can relaunch is straight afterwards
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    server.queue = queue

    return server


def launch_client(data):
    global server_busy

    server_busy = True

    HOST, PORT = "localhost", 9959
    json_data = json.dumps(data)

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(json_data)

        # Receive data from the server and shut down
        received1 = sock.recv(4096)
        server_busy = (received1 == 'busy')
        received2 = sock.recv(4096)
        server_busy = (received2 == 'busy')
    finally:
        sock.close()
