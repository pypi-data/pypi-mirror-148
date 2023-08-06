import json
import sys

from descripts import SetName


class Handler:
    """Main class responsible for sending and receiving messages"""

    username = SetName()

    def __init__(self):
        self.message = {}
        self.username = 'Guest'
        self.sock = None

    def send_message(self):
        json_message = json.dumps(self.message)
        self.sock.send(json_message.encode('utf-8'))

    def get_message(self):
        encoded_response = self.sock.recv(1024)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode('utf-8')
            if not json_response:
                sys.exit()
            response = json.loads(json_response)
            if isinstance(response, dict):
                self.message = response
            else:
                raise Exception
        else:
            raise Exception
