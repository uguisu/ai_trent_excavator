# coding=utf-8
# author xin.he

from enum import Enum


class StandardMessageCode(Enum):
    """
    Standard Message Code
    """
    # error
    E_100_9000_000001 = (1009000000001, '{db} database connection failed')
    E_100_9000_000002 = (1009000000002, 'Can not find config file {cfg_file_name}')

    # warning
    W_100_9000_100001 = (1009000100001, 'Exception occurs while closing database connection')

    # info
    I_100_9000_200001 = (1009000200001, 'Connecting database: {host}:{port}')
    I_100_9000_200002 = (1009000200002, 'Database connected')
    I_100_9000_200003 = (1009000200003, 'Database disconnected')
    I_100_9000_200004 = (1009000200004, 'Server listening on {host}:{port}')
    I_100_9000_200005 = (1009000200005, 'Find {db_name} connection info')
    I_100_9000_200006 = (1009000200006, 'Reading {file_name}')
    # I_100_9000_200006 = (1009000200006, 'call {method_name} start')
    # I_100_9000_200007 = (1009000200007, 'call {method_name} end')

    def get_code(self):
        return self.value[0]

    def get_msg(self):
        return self.value[1]

    def get_formatted_msg(self, **info):
        if info:
            msg = self.value[1].format_map(info)
            return '[{code}] {msg}'.format(code=self.value[0], msg=msg)
        return '[{code}] {msg}'.format(code=self.value[0], msg=self.value[1])
