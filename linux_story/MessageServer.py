# MessageServer.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Controls communicating between the GUI and the terminal
import socket
import threading
import Queue
import SocketServer
import time
import traceback

from linux_story.MyTCPHandler import MyTCPHandler
from linux_story.dependencies import Logger


class MessageServer:
    HOST = "localhost"
    PORT = 9959

    def __init__(self, queue, window):
        self.__window = window
        self.__server_busy = False
        SocketServer.TCPServer.allow_reuse_address = True
        self.__server = SocketServer.TCPServer((MessageServer.HOST, MessageServer.PORT), MyTCPHandler)
        self.__server.queue = queue
        self.__is_busy = False

    def start_in_separate_thread(self):
        t = threading.Thread(target=self.__server.serve_forever)
        t.start()

    def shutdown(self, widget=None, event=None):
        self.__server.socket.shutdown(socket.SHUT_RDWR)
        self.__server.socket.close()
        self.__server.shutdown()

    def check_queue(self):
        try:
            self.__is_busy = True
            data_dict = self.__server.queue.get(False, timeout=5.0)
            if 'exit' in data_dict.keys():
                self.__window.finish_app()
                return False
            elif 'hint' in data_dict.keys():
                self.__window.show_hint(data_dict["hint"])
            elif 'challenge' in data_dict.keys() and 'story' in data_dict.keys() and 'spells' in data_dict.keys():
                self.__window.start_new_challenge(data_dict)

            self.__is_busy = False

        except Queue.Empty:
            pass
        except Exception:
            Logger.error('Unexpected error in MainWindow: check_queue: - [{}]'.format(traceback.format_exc()))
        finally:
            time.sleep(0.02)
            return True

    def check_if_busy(self):
        # have a socket to query?
        return self.__is_busy
