#!/usr/bin/env python

# socket_functions.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Create server so terminal and GUI can communicate with each other

import SocketServer
import socket
import json
import threading
import time


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
        self.data = self.request.recv(1024).strip()
        data_dict = json.loads(self.data)
        self.server.queue.put(data_dict)


def create_server(queue):  # text_cb, spell_cb, challenge_cb):
    HOST, PORT = "localhost", 9959

    # Create the server, binding to localhost on port 9999

    # Magic line that allows you to reuse the address, even if a
    # different server is using it.  This means if we launch this and then
    # quit it, we can relaunch is straight afterwards
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    server.queue = queue

    return server


def launch_server(story_cb, hint_cb, arg):
    server = create_server(story_cb, hint_cb, arg)
    server.serve_forever()


def launch_client(data):
    global server_busy

    HOST, PORT = "localhost", 9959
    json_data = json.dumps(data)

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(json_data + "\n")

        # Receive data from the server and shut down
        received1 = sock.recv(1024)
        server_busy = (received1 == 'busy')
        received2 = sock.recv(1024)
        server_busy = (received2 == 'busy')
    finally:
        sock.close()


def sleep(arg=None, arg2=None):
    time.sleep(5)


if __name__ == '__main__':
    t1 = threading.Thread(target=launch_server, args=(sleep, sleep, None))
    t1.start()

    time.sleep(0.5)

    t2 = threading.Thread(target=launch_client, args=({'hint': "hunteaffadf"},))
    t2.start()
