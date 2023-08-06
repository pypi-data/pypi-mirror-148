import binascii
import hmac
import os
import threading
from select import select
from socket import socket, AF_INET, SOCK_STREAM

from server.server.common.handler import Handler
from server.server.common.descripts import CheckPort, CheckIp
from server.server.common.metaclasses import CheckStatus
from login_required import login_required


class Server(threading.Thread, metaclass=CheckStatus):
    listen_port = CheckPort()
    ip_address = CheckIp()
    """
    The main server class. Accepts connections, packages
    from clients, processes incoming messages.
    """

    def __init__(self, ip_address, port, database):
        super().__init__()
        self.ip_address = ip_address
        self.listen_port = port
        self.database = database
        self.clients = []
        self.messages = None
        self.users = {}

    def run(self):
        """Main thread loop"""

        print(f'Address: {self.ip_address}\nPort: {self.listen_port}')

        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.ip_address, self.listen_port))
        sock.settimeout(0.5)

        sock.listen()

        while True:

            try:
                client, client_address = sock.accept()
            except OSError:
                pass
            else:
                print(f'The client {client_address} connected')
                self.clients.append(client)
            receive_data = []
            try:
                if self.clients:
                    receive_data, self.messages, errors = select(self.clients,
                                                                 self.clients,
                                                                 [], 0)
            except Exception as e:
                print(e)

            if receive_data:
                for clients_message in receive_data:
                    try:
                        handler = Handler()
                        handler.sock = clients_message
                        handler.get_message()
                        message = handler.message
                        self.client_message_handler(message, clients_message,
                                                    handler)
                    except Exception as e:
                        print(f'Error: {e}')
                        print(
                            f'Client {clients_message.getpeername()}'
                            f' was disconnected')
                        for user in self.users:
                            if self.users[user] == clients_message:
                                self.remove_user({'user': user},
                                                 clients_message)
                                break
                        if clients_message in self.clients:
                            self.clients.remove(clients_message)

    def add_users(self, user, message, sock):
        """Handler for adding authorized users to the shared dictionary"""

        client_ip, client_port = sock.getpeername()
        self.users[message['user']] = sock
        self.database.user_history(user, client_ip, client_port,
                                   status='login')
        self.database.add_active_users(user, client_ip, client_port)

    def remove_user(self, message, sock):
        """The handler of the client with which
        communication was interrupted.
        """

        client_ip, client_port = sock.getpeername()
        self.clients.remove(sock)
        self.users[message['user']].close()
        del self.users[message['user']]
        self.database.remove_active_users(message['user'])
        self.database.user_history(message['user'], client_ip, client_port,
                                   None)
        print(f'Client {client_ip}, {client_port} disconnected')

    @login_required
    def client_message_handler(self, message, client, handler):
        """Incoming message handler."""

        user = message['user']

        if message['action'] == 'presence':
            handler.message = {'OK': 'Server status OK: 200'}
            handler.send_message()

        elif message['action'] == 'registration':
            user = message['user']
            password = message['password']
            if self.database.create_user(user, password):
                handler.message = {'action': 'registered', 'user': user}
                handler.send_message()
                self.add_users(user, message, client)
            else:
                handler.message = {
                    'action': 'refuse',
                    'response': f'Sorry the name: {user}'
                                f' already exists.\n Please try again'
                }
                handler.send_message()

        elif message['action'] == 'authorisation':
            if self.database.check_username(user):
                handler.message = {
                    'action': None,
                    'response': f'Sorry the name: {user}'
                                f' is absent.\n Please try again'
                }
                handler.send_message()
            else:
                random_str = binascii.hexlify(os.urandom(64))
                server_hash = hmac.new(self.database.get_password(user),
                                       random_str, 'MD5')
                digest = server_hash.digest()
                handler.message = {
                    'user': user,
                    'data': random_str.decode('ascii'),
                    'response': 511
                }
                try:
                    handler.send_message()
                    handler.get_message()
                except OSError as e:
                    print(e)
                client_digest = binascii.a2b_base64(handler.message['data'])
                if handler.message['response'] == 511 and hmac.compare_digest(
                        digest, client_digest):
                    if user not in self.users.keys():
                        self.add_users(user, message, client)
                        handler.message = {
                            'action': 'success',
                            'user': user,
                            'response': 'User is authorized'
                        }
                        handler.send_message()
                else:
                    handler.message = {
                        'action': 'wrong_password',
                        'user': user,
                        'response': 'Wrong password. Please try again'
                    }
                    handler.send_message()

        elif message['action'] == 'update_key':
            self.database.update_key(user, message['key'])

        elif message['action'] == 'message':
            if message['addressee'] in self.users and self.users[
               message['addressee']] in self.messages:
                self.database.add_message_history(user, message['addressee'],
                                                  message['message'],
                                                  action='sent')
                response = self.database.message_count(user)
                handler.message = {
                    'action': 'sent_message',
                    'user': user,
                    'addressee': message['addressee'],
                    'count': response[0],
                    'message': message['message']
                }
                handler.send_message()

                self.database.add_message_history(user, message['addressee'],
                                                  message['message'],
                                                  action='')
                response = self.database.message_count(message['addressee'])
                handler.message = {
                    'action': 'message',
                    'user': user,
                    'addressee': message['addressee'],
                    'count': response[1],
                    'message': message['message']
                }
                handler.sock = self.users[message['addressee']]
                handler.send_message()
                handler.sock = client

            elif message['addressee'] in self.users and self.users[
                 message['addressee']] not in self.messages:
                print(
                    f'Connection with client {message["addressee"]} was lost')
            else:
                print(f'User {message["addressee"]} does not registered')

        elif message['action'] == 'get_contacts' and self.users[
             user] == client:
            response = self.database.get_contacts(user)
            if response:
                handler.message = {
                    'action': 'got_contacts',
                    'response': response
                }
                handler.send_message()
            else:
                handler.message = {
                    'action': 'no_contact',
                    'response': "You don't have any contact"
                }
                handler.send_message()

        elif message['action'] == 'add_contact' and self.users[user] == client:
            response = self.database.add_contact(user, message['contact'])
            if response:
                if response == 'no_contact':
                    handler.message = {
                        'action': 'no_contact',
                        'response': 'There is no such contact in the database'
                    }
                    handler.send_message()
                else:
                    handler.message = {
                        'action': 'added_contact',
                        'contact': message['contact'],
                        'response': f'The contact {message["contact"]}'
                                    f' was added'
                    }
                    handler.send_message()
            else:
                handler.message = {
                    'action': 'exist_contact',
                    'response': f'Sorry, the {message["contact"]}'
                                f' already exists'
                }
                handler.send_message()

        elif message['action'] == 'del_contact' and self.users[user] == client:
            response = self.database.del_contact(user, message['contact'])
            if response:
                if response == 'no_contact':
                    handler.message = {
                        'action': 'no_contact',
                        'response': 'There is no such contact'
                                    ' in your contact list'
                    }
                    handler.send_message()
                else:
                    handler.message = {
                        'action': 'deleted_contact',
                        'response': f'The contact {message["contact"]}'
                                    f' was deleted',
                        'contact': message['contact']
                    }
                    handler.send_message()
            else:
                handler.message = {
                    'action': 'no_contact',
                    'response': 'There is no such contact in the database'
                }
                handler.send_message()

        elif message['action'] == 'all_users':
            response = self.database.get_all_users()
            handler.message = {
                'action': 'got_all_users',
                'response': response
            }
            handler.send_message()

        elif message['action'] == 'get_contact_key':
            key = self.database.get_key(message['contact'])
            if key:
                handler.message = {
                    'action': 'got_contact_key',
                    'key': key,
                    'response': 511
                }
                handler.send_message()
            else:
                handler.message = {'response': 400}
                handler.send_message()

        elif message['action'] == 'exit':
            if user == 'Guest':
                self.clients.remove(client)
                print(f'Client {client.getpeername()} was disconnected')
            else:
                self.remove_user(message, client)
        else:
            print('Error: No action')
