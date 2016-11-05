# Server controls the Gtk window
import sys
import traceback

from flask import Flask, jsonify

from linux_story.gtk3.MainWindow import MainWindow

app = Flask(__name__)
port = 9959
window = None


@app.route("/")
def hello():
    print "/ hit"
    return "Hello World!"


@app.route("/hint/<text>")
def show_hint(text):
    print "/hint hit"
    print text
    # window.show_hint(hint_text)
    try:
        window.add_hint_to_queue(str(text))
        return jsonify(result={"status": 200})
    except Exception as e:
        print "exception " + e.message;
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)


@app.route("/challenge/<int:number>")
def start_challenge(number):
    try:
        print "/challenge hit"
        # get data about what info to show?
        # window.start_challenge(number)
        window.add_start_new_challenge_to_queue(number, "blah", ["cd"])
        return jsonify(result={"status": 200})
    except Exception as e:
        print "exception " + e.message;


@app.route("/busy")
def get_if_server_busy():
    try:
        print "/busy hit"
        return window.is_busy
        return jsonify(result={"status": 200})
    except Exception as e:
        print "exception " + e.message;


@app.route("/exit")
def close_window():
    # window.exit()
    print "exiting app"


def run(**kwargs):
    global window

    window = kwargs["window"]
    print window
    return app.run(port=port, host="127.0.0.1", threaded=True)


def get_window():
    # not sure this is needed
    return window

# if __name__ == "__main__":
#     app.run(port=9959)

'''
# MessageServer.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Controls communicating between the GUI and the terminal


import threading
import socket
import Queue
import SocketServer
import json
from linux_story.dependencies import Logger
from linux_story.MyTCPHandler import MyTCPHandler


class MessageServer:
    HOST = "localhost"
    PORT = 9959

    def __init__(self):
        self.__server_busy = False
        self.__queue = Queue.Queue(1)
        self.__server = self.__create_server()
        t = threading.Thread(target=self.__server.serve_forever)
        t.daemon = True
        t.start()

    def get_data(self):
        return self.__queue.get(False, timeout=5.0)

    def send_text(self, string):
        if not self.__server_busy:
            data = {'hint': string}
            t = threading.Thread(target=self.__launch_client, args=(data,))
            t.daemon = True
            t.start()

    def __create_server(self):
        # Magic line that allows you to reuse the address, even if a different server is using it.
        # This means if we launch this and then quit it, we can relaunch is straight afterwards
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer((MessageServer.HOST, MessageServer.PORT), MyTCPHandler)
        server.queue = self.__queue
        return server

    def __launch_client(self, data):
        self.__server_busy = True
        json_data = json.dumps(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((MessageServer.HOST, MessageServer.PORT))
            sock.sendall(json_data)
            received1 = sock.recv(4096)
            self.__server_busy = (received1 == 'busy')
            received2 = sock.recv(4096)
            self.__server_busy = (received2 == 'busy')
        finally:
            sock.close()

    def __finish_if_server_ready(self, other_condition):
        Logger.debug("server_busy = {}".format(self.__server_busy))
        Logger.debug('other_condition = {}'.format(other_condition))
        will_finish = (not self.__server_busy and other_condition)
        Logger.debug('will finish = {}'.format(will_finish))
        return will_finish
'''
