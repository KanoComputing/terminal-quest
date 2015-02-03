import SocketServer
import socket
import json
import threading
import time
from gi.repository import GObject


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

        text_cb = self.server.win.type_text
        spell_cb = self.server.win.repack_spells
        challenge_cb = self.server.win.print_challenge_title

        self.request.sendall('busy')

        # Type out the hint
        if 'hint' in data_dict.keys():
            text_cb(data_dict['hint'])
            self.request.sendall('ready')
        else:

            self.server.win.story.clear()

            if 'challenge' in data_dict.keys() and \
               'story' in data_dict.keys() and \
               'spells' in data_dict.keys():

                # Print the challenge title at the top of the screen
                challenge = data_dict['challenge']
                GObject.idle_add(challenge_cb, challenge)

                # Type the story out
                text_cb(data_dict['story'])

                # Repack the spells into the spellbook
                spells = data_dict['spells']
                GObject.idle_add(spell_cb, spells)

                self.request.sendall('ready')


def create_server(window):  # text_cb, spell_cb, challenge_cb):
    HOST, PORT = "localhost", 9959

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.win = window
    return server


def launch_server(story_cb, hint_cb, arg):
    server = create_server(story_cb, hint_cb, arg)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    #server.serve_forever()
    server.handle_request()


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
