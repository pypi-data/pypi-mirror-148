import dis


class CheckStatus(type):
    def __init__(cls, name, base, attrs):
        super().__init__(name, base, attrs)
        print(f'{name} started...')
        load_global = []
        for i in attrs:
            try:
                ret = dis.get_instructions(attrs[i])
            except TypeError:
                pass
            else:
                for j in ret:
                    if j.opname == 'LOAD_GLOBAL':
                        if j.argval not in load_global:
                            load_global.append(j.argval)
        # print(load_global)

        if name == 'Server':
            if 'connect' in load_global:
                raise TypeError('Using connect method is not allowed'
                                ' in server class')
            if not ('SOCK_STREAM' in load_global and 'AF_INET' in load_global):
                raise TypeError('Incorrect socket initialization')

        elif name == 'Client':
            if 'accept' in load_global or 'listen' in load_global:
                raise TypeError('The use of a forbidden method was detected'
                                ' in the class')
            if not ('SOCK_STREAM' in load_global and 'AF_INET' in load_global):
                raise TypeError('Incorrect socket initialization')
