# socket_functions.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Create server so terminal and GUI can communicate with each other

import json
import SocketServer


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
        data = self.request.recv(4096).strip()
        self.server.queue.put(json.loads(data))
