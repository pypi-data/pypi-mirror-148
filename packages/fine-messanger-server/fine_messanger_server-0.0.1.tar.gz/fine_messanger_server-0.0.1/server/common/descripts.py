import ipaddress


class CheckPort:
    """Handle responsible for checking the correct port"""

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):

        if not 1023 < value < 65536:
            raise ConnectionError(f'Incorrect port "{value}".'
                                  f' The port must be between 1023 and 65536.')
        instance.__dict__[self.name] = value


class CheckIp:
    """Handle responsible for checking the correct ip address"""

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if value == '':
            value = '127.0.0.1'
        try:
            ipaddress.ip_address(value)
            instance.__dict__[self.name] = value
        except ValueError as e:
            print(f'Error: {e}')
            exit(1)


class SetName:
    """Handle responsible for checking the correct username"""

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if 1 < len(value) < 20:
            instance.__dict__[self.name] = value
        else:
            instance.__dict__[self.name] = None
