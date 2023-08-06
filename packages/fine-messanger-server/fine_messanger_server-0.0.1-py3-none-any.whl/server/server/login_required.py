from socket import socket


def login_required(func):
    """A decorator that checks that the client is authorized on the server.
    Verifies that the socket object being passed is in
    list of authorized clients.
    Except for passing a query dictionary
    for authorization. If the client is not authorized,
    throws a TypeError exception
    """

    def checker(*args, **kwargs):
        from core import Server

        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket):
                    for client in args[0].users:
                        if args[0].users[client] == arg:
                            found = True
            for arg in args:
                if isinstance(arg, dict):
                    if 'action' in arg and arg['action'] == 'presence'\
                            or arg['action'] == 'authorisation'\
                            or arg['action'] == 'registration':
                        found = True
            if not found:
                raise TypeError
        return func(*args, **kwargs)
    return checker
