# coding=utf-8
# author xin.he
import logging

import shares
from config import args
from config import load_config
from shares.message_code import StandardMessageCode
from skate_thread.skate_process import ScheduledFixedProcessPool
from shares.time_util import get_current_date_time

# ============================================================
# declare parameter
# ============================================================
# database connection
db_connection = None
process_pool: ScheduledFixedProcessPool = None

# logger
logger = logging.getLogger('skATE')
logger.setLevel(logging.INFO)

# show logo
shares.show_logo()

# read config
config_info_entity = load_config(args)

# make sure packages
shares.make_sure_packages(config_info_entity)

# ============================================================
# main process
# NOTICE: DO NOT MOVE FOLLOWING 'IMPORT' CODE TO THE TOP
# ============================================================
import os
from cheroot.wsgi import PathInfoDispatcher, Server
from flask import Flask

import static_info

# declare application object
skate_app = Flask(__name__)
skate_app.config['SECRET_KEY'] = os.urandom(24)


@skate_app.route('/serviceList', methods=['GET'])
def get_service_list():
    """
    get service list
    """
    return {
        "services": [1, 2, 3]
    }


@skate_app.route('/api/1/declareService/<string:al_id>', methods=['GET'])
def declare_service(al_id):
    """
    declare service

    :param al_id: algorithm id

    :return: real process id, if success. This id should be used as key word for further prediction
    """

    global logger

    method_name = 'declare_service'
    logger.info(StandardMessageCode.I_100_9000_200012.get_formatted_msg(method_name=method_name))

    # get real class
    from algorithm.algorithm_map import algorithm_map
    al_class = algorithm_map.get(al_id)

    if al_class is None:
        # target algorithm do not exist
        logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))
        return StandardMessageCode.W_100_9000_100004.get_formatted_msg(algorithm_id=al_id)

    # get name
    _process_id = f'{al_id}-{get_current_date_time()}'
    # get instance
    exec(f'from {al_class.package_name} import {al_class.class_name}')
    _process_obj = eval(f'{al_class.class_name}(logger, "{_process_id}")')
    process_pool.add_job(_process_obj)

    # logger.info(f'from main name: {__name__}')
    logger.info(f'from main parent process id: {os.getppid()}')
    logger.info(f'from main process id: {os.getpid()}')

    logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))

    return _process_id


@skate_app.route('/api/1/getVal/<string:process_id>', methods=['GET'])
def get_val(process_id):
    """
    get predict value by process id

    :param process_id: process id. This id is the return value of the declare_service() function

    :return: predicted value
    """
    global logger

    method_name = 'get_val'
    logger.info(StandardMessageCode.I_100_9000_200012.get_formatted_msg(method_name=method_name))

    _tmp_p = process_pool.get_process_by_name(process_id)

    logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))

    return _tmp_p.predict('from get val')


def init_env():
    """
    init environment
    """

    global config_info_entity, logger, db_connection, process_pool

    # log file =====
    _log_formatter = logging.Formatter(static_info.LOG_FORMAT_STR)
    _file_handler = logging.FileHandler('./AiOps.log', mode='w', encoding='utf-8')
    _file_handler.setFormatter(_log_formatter)
    logger.addHandler(_file_handler)

    _console_handler = logging.StreamHandler()
    _console_handler.setFormatter(_log_formatter)
    logger.addHandler(_console_handler)

    # determine database
    if config_info_entity.es_host is not None:
        # connect to ES
        logger.info(StandardMessageCode.I_100_9000_200005.get_formatted_msg(db_name='ElasticSearch'))
        # Connecting database
        logger.info(StandardMessageCode.I_100_9000_200001.get_formatted_msg(host=config_info_entity.es_host,
                                                                            port=config_info_entity.es_port))
        # setup flag
        static_info.DATA_SOURCE_FLG = static_info.DataSourceEnum.ES

        from elasticsearch import Elasticsearch
        db_connection = Elasticsearch(
            # ["192.168.11.16", "192.168.11.xxxx"], 连接集群，以列表的形式存放各节点的IP地址
            [f'http://{config_info_entity.es_host}:{config_info_entity.es_port}'],
            sniff_on_start=True,
            sniff_on_node_failure=True,
            sniff_timeout=60
        )

        # TODO debug
        print(db_connection.info)
        import elasticsearch
        try:
            print(db_connection.search(index='news'))
        except elasticsearch.NotFoundError:
            print('I know not found')

    else:
        # connect to mysql
        logger.info(StandardMessageCode.I_100_9000_200005.get_formatted_msg(db_name='MySql'))
        # Connecting database
        logger.info(StandardMessageCode.I_100_9000_200001.get_formatted_msg(host=config_info_entity.mysql_host,
                                                                            port=config_info_entity.mysql_port))
        from data_mysql import MySQLConnector
        db_connection = MySQLConnector(config_info_entity, logger).open_db_connection()
        # setup flag
        static_info.DATA_SOURCE_FLG = static_info.DataSourceEnum.MySQL

    # open process pool
    # TODO move pool_size to config file
    process_pool = ScheduledFixedProcessPool(logger, pool_size=10)

    # Database connected
    logger.info(StandardMessageCode.I_100_9000_200002.get_formatted_msg())


def release_env():
    """
    release environment
    """

    global db_connection, process_pool

    try:
        if static_info.DATA_SOURCE_FLG is static_info.DataSourceEnum.MySQL:
            db_connection.dispose()
        else:
            # TODO not sure
            # db_connection.transport.connection_pool.close()
            db_connection.close()
    except Exception:
        # Exception occurs while closing database connection
        logger.warning(StandardMessageCode.W_100_9000_100001.get_formatted_msg())

    # release process_pool
    if process_pool is not None and process_pool.job_amount >= 0:
        _p = process_pool.stop_all_process()
        del process_pool

    # Database disconnected
    logger.info(StandardMessageCode.I_100_9000_200003.get_formatted_msg())


if __name__ == '__main__':

    init_env()

    # start http server
    server = Server((config_info_entity.http_binding_address, int(config_info_entity.http_binding_port)),
                    PathInfoDispatcher({'/': skate_app}))

    # server get ready
    logger.info(StandardMessageCode.I_100_9000_200004.get_formatted_msg(host=config_info_entity.http_binding_address,
                                                                        port=config_info_entity.http_binding_port))

    try:
        server.start()
    except KeyboardInterrupt:
        # release environment
        release_env()
        server.stop()
