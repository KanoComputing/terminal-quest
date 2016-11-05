# This communicates from the terminal
import requests


class Client():
    def __init__(self):
        self.__url = "localhost:9959"

    def send_hint(self, text):
        url = self.__url + "/hint"
        data = '{"hint": ' + text + '}'
        requests.post(url, data=data)
