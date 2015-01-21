#!/usr/bin/env python

# socket_functions.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Functions that use sockets to send data


import socket
import select
from file_functions import append_to_file


PORT_NUMBERS = {
    "story": 50008,
    "commands": 50009,
    "output": 50010,
    "started": 50011,
    "challenge": 50012,
    "exit": 50013,
    "hint": 50014
}


def socket_client(message, port):
    HOST = ''    # The remote host
    PORT = port              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message)
    data = s.recv(1024)
    s.close()
    print 'Received', repr(data)


def socket_server(port):
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = port              # Arbitrary non-privileged port
    data_received = None

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        else:
            conn.sendall(data)
            data_received = data

    conn.close()
    return data_received


def server_multiple_ports():
    import sys

    sock_lst = []
    host = ''
    backlog = 5  # Number of clients on wait.
    buf_size = 1024

    try:
        for name, number in PORT_NUMBERS.iteritems():
            sock_lst.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            sock_lst[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_lst[-1].bind((host, number))
            sock_lst[-1].listen(backlog)
    except socket.error, (value, message):
        if sock_lst[-1]:
            sock_lst[-1].close()
            sock_lst = sock_lst[:-1]
        print 'Could not open socket: ' + message
        sys.exit(1)

    while True:
        read, write, error = select.select(sock_lst, [], [])

        for r in read:
            for item in sock_lst:
                if r == item:
                    accepted_socket, adress = item.accept()

                    print 'We have a connection with ', adress
                    data = accepted_socket.recv(buf_size)
                    if data:
                        print data
                        accepted_socket.send('Hello, and goodbye.')
                    accepted_socket.close()


class Server():

    def __init__(self):
        import sys

        self.sock_lst = []
        self.host = ''
        self.backlog = 5  # Number of clients on wait.
        self.buf_size = 1024

        try:
            for name, number in PORT_NUMBERS.iteritems():
                print 'trying to create port for name = {}'.format(name)
                self.sock_lst.append(
                    socket.socket(
                        socket.AF_INET,
                        socket.SOCK_STREAM
                    )
                )
                self.sock_lst[-1].setsockopt(
                    socket.SOL_SOCKET,
                    socket.SO_REUSEADDR,
                    1
                )
                self.sock_lst[-1].bind((self.host, number))
                self.sock_lst[-1].listen(self.backlog)
        except socket.error, (value, message):
            if self.sock_lst[-1]:
                self.sock_lst[-1].close()
                self.sock_lst = self.sock_lst[:-1]
            print 'Could not open socket for ' + name + ': ' + message
            sys.exit(1)

    def read_message(self):
        read, write, error = select.select(self.sock_lst, [], [])

        for r in read:
            for item in self.sock_lst:
                if r == item:
                    accepted_socket, adress = item.accept()

                    print 'We have a connection with ', adress
                    data = accepted_socket.recv(self.buf_size)
                    if data:
                        print data
                        accepted_socket.send('Hello, and goodbye.')
                    accepted_socket.close()


def send_message(subject, message):
    append_to_file('debug', 'Entered send_message, subject {}'.format(subject))
    append_to_file('debug', 'Entered send_message, message {}'.format(message))
    try:
        print 'sending message, subject {}'.format(subject)
        port = PORT_NUMBERS[subject]
        socket_client(message, port)

        # succeeded
        return True
    except socket.error, e:
        if str(e) == '[Errno 111] Connection refused':
            print 'Subject {} probably is not open'.format(subject)
            append_to_file('debug', 'Subject {} probably is not open'.format(subject))
        else:
            print '\'{}\''.format(e)

        # failed
        return False


def read_message(subjects):
    import sys

    append_to_file('debug', 'Entered read_message')
    append_to_file('debug', 'Subjects = {}'.format(subjects))
    if type(subjects) == str:
        subjects = [subjects]

    sock_dict = {}
    sock_lst = []
    host = ''
    backlog = 5  # Number of clients on wait.
    buf_size = 1024

    try:
        for name, number in PORT_NUMBERS.iteritems():
            if name in subjects:
                sock_dict[name] = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )
                sock_dict[name].setsockopt(
                    socket.SOL_SOCKET,
                    socket.SO_REUSEADDR,
                    1
                )
                sock_dict[name].bind((host, number))
                sock_dict[name].listen(backlog)
                sock_lst.append(sock_dict[name])

    except socket.error, (value, message):
        if sock_dict[name]:
            sock_dict[name].close()
            del sock_dict[name]
        append_to_file('debug', 'Could not open socket: ' + message)
        print 'Could not open socket: ' + message
        sys.exit(1)

    read, write, error = select.select(sock_lst, [], [])

    for r in read:
        for s in subjects:
            if r == sock_dict[s]:
                item = sock_dict[s]
                accepted_socket, adress = item.accept()

                print 'We have a connection with ', adress
                data = accepted_socket.recv(buf_size)
                print 'data = {}'.format(data)
                chosen_subject = s
                if data:
                    accepted_socket.send(chosen_subject)
                accepted_socket.close()

    if data:
        return chosen_subject + ' ' + data


#def read_message(subject):
#    print 'looking for subject {} message'.format(subject)
#    port = PORT_NUMBERS[subject]
#    print 'port = {}'.format(port)
#    message = socket_server(port)
#    print 'finished looking for message'
#    return message
