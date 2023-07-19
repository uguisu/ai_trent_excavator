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
    # E_100_9000_000003 = (1009000000003, 'Please train model before predict')
    E_100_9000_000004 = (1009000000004, 'Invalid parameter: {parameter_name}')
    E_100_9000_000005 = (1009000000005, '{method_name} has not been implemented yet')
    E_100_9000_000006 = (1009000000006, 'The thread pool is currently unavailable')

    # warning
    W_100_9000_100001 = (1009000100001, 'Exception occurs while closing database connection')
    W_100_9000_100002 = (1009000100002, 'The thread pool is full')
    W_100_9000_100003 = (1009000100003, 'Target job do not exist. name = {job_name}')
    W_100_9000_100004 = (1009000100004, 'Target algorithm do not exist. name = {algorithm_id}')
    W_100_9000_100005 = (1009000100005, 'Cannot find valid model')
    W_100_9000_100006 = (1009000100006, 'GPU device is currently unavailable, use CPU instead')

    # info
    I_100_9000_200001 = (1009000200001, 'Connecting database: {host}:{port}')
    I_100_9000_200002 = (1009000200002, 'Database connected')
    I_100_9000_200003 = (1009000200003, 'Database disconnected')
    I_100_9000_200004 = (1009000200004, 'Server listening on {host}:{port}')
    I_100_9000_200005 = (1009000200005, 'Find {db_name} connection info')
    I_100_9000_200006 = (1009000200006, 'Reading {file_name}')
    I_100_9000_200007 = (1009000200007, 'From {program_name}:\nparent process id -> {pp_id}\n'
                                        '\t\t┗ local process id -> {l_id}')
    I_100_9000_200008 = (1009000200008, 'Generating job with name: {job_name}')
    I_100_9000_200009 = (1009000200009, 'Get job by name: {job_name}')
    I_100_9000_200010 = (1009000200010, 'Stop job by name: {job_name}')
    I_100_9000_200011 = (1009000200011, 'All job stopped')
    I_100_9000_200012 = (1009000200012, 'Call {method_name}() start')
    I_100_9000_200013 = (1009000200013, 'Call {method_name}() end')
    I_100_9000_200014 = (1009000200014, 'CUDA version: {cuda_version}')


    def get_code(self):
        return self.value[0]

    def get_msg(self):
        return self.value[1]

    def get_formatted_msg(self, **info):
        if info:
            msg = self.value[1].format_map(info)
            return '[{code}] {msg}'.format(code=self.value[0], msg=msg)
        return '[{code}] {msg}'.format(code=self.value[0], msg=self.value[1])
