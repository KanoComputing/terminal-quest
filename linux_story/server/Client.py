# This communicates from the terminal
import requests


class Client:
    def __init__(self):
        self.__url = "localhost:9959"

    def send_hint(self, text):
        print "client: sending hint"
        url = self.__url + "/hint"
        data = '{"hint": ' + text + '}'
        requests.post(url, data=data)

    def send_start_challenge_data(self, story, challenge_num, commands, highlighted_commands):
        print "client: sending start_challenge data"
        url = self.__url + "/challenge/" + challenge_num
        data = '{"story": ' + story + \
               ', "commands":' + commands + \
               ', "highlighted_commands: " + ' + highlighted_commands + '}'
        requests.post(url, data=data)
