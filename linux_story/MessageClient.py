# MessageClient.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The functions which starts off the game at the specified challenge and step.


from kano.logging import logger
import json
import socket


class MessageClient:
    HOST = "localhost"
    PORT = 9959

    def __init__(self):
        self.__server_busy = False

    def exit(self):
        self.__send_message({"exit": 1})

    def set_dark_theme(self):
        self.__send_message({"dark": True})

    def set_normal_theme(self):
        self.__send_message({"dark": False})

    def send_hint(self, string):
        self.send_text(string)

    def send_start_challenge_data(self, story, challenge, spells, highlighted, xp, print_text):
        data = {
            "story": story,
            "challenge": challenge,
            "spells": spells,
            "highlighted": highlighted,
            "xp": xp
        }
        if print_text:
            data["print_text"] = print_text

        self.__send_message(data)

    def send_text(self, string):
        if not self.__server_busy:
            self.__send_message({'hint': string})

    def __send_message(self, data):
        self.__server_busy = True
        json_data = json.dumps(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((MessageClient.HOST, MessageClient.PORT))
            sock.sendall(json_data)
            received1 = sock.recv(4096)
            self.__server_busy = (received1 == 'busy')
            received2 = sock.recv(4096)
            self.__server_busy = (received2 == 'busy')
        finally:
            sock.close()

    def finish_if_server_ready(self, other_condition):
        logger.debug("server_busy = {}".format(self.__server_busy))
        logger.debug('other_condition = {}'.format(other_condition))
        will_finish = (not self.__server_busy and other_condition)
        logger.debug('will finish = {}'.format(will_finish))
        return will_finish
