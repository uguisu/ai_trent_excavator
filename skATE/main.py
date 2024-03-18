# coding=utf-8
# author xin.he
import logging

from skATE import shares
from skATE.config import load_config, args
from skATE.shares.message_code import StandardMessageCode
from skATE.shares.skate_enum import DebugLevel, AlgorithmMetaDataMap, AlgorithmMetaDataParameter
from skATE.shares.time_util import get_current_date_time
from skATE.skate_thread.skate_process import ScheduledFixedProcessPool

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
shares.make_sure_packages(config_info_entity, logger)

# ============================================================
# main process
# NOTICE: DO NOT MOVE FOLLOWING 'IMPORT' CODE TO THE TOP
# ============================================================
import os
import static_info
import numpy as np

from cheroot.wsgi import PathInfoDispatcher, Server
from flask import Flask, json, request
from flasgger import Swagger, swag_from

from skATE.shares.api_interfaces import BaseRsp

# declare application object
skate_app = Flask(__name__)
skate_app.config['SECRET_KEY'] = os.urandom(24)
skate_app.config['SWAGGER'] = {
    'title': 'AI Trent Excavator (skate)',
    'uiversion': 3,
    'version': f'{static_info.__version__}',
    'description': 'AI Trent Excavator for Apache Skywalking.',
    'termsOfService': 'https://github.com/uguisu/ai_trent_excavator'
}
# swagger
Swagger(skate_app)


@skate_app.route('/serviceList', methods=['GET'])
def get_service_list():
    """
    get service list
    """
    return {
        "services": [1, 2, 3]
    }


@skate_app.route('/api/1/getServiceParameter/<string:al_id>', methods=['GET'])
# TODO
# @swag_from('yaml/getServiceParameter.yaml')
def get_service_parameter(al_id):
    """
    get algorithm service parameter

    :param al_id: algorithm id

    :return: algorithm service parameter as metadata map
    """

    global logger

    method_name = 'get_service_parameter'
    logger.info(StandardMessageCode.I_100_9000_200012.get_formatted_msg(method_name=method_name))

    # get real class
    from algorithm.algorithm_map import algorithm_map
    al_class = algorithm_map.get(al_id).get(AlgorithmMetaDataMap.ALGORITHM_CLS.value)

    # get instance
    exec(f'from {al_class.package_name} import {al_class.class_name}')
    # get metadata
    wrk_metadata = eval(f'{al_class.class_name}.metadata()')

    rtn = BaseRsp(wrk_metadata, True, None).to_dict()

    logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))

    return rtn


@skate_app.route('/api/1/declareService/<string:al_id>', methods=['POST'])
@swag_from('yaml/declareService.yaml')
def declare_service(al_id):
    """
    declare algorithm service

    :param al_id: algorithm id

    :return: real process id, if success. This id should be used as key word for further prediction
    """

    global logger, db_connection

    method_name = 'declare_service'
    logger.info(StandardMessageCode.I_100_9000_200012.get_formatted_msg(method_name=method_name))

    # parse & verify input data
    algorithm_param = json.loads(request.data).get(AlgorithmMetaDataParameter.ALGORITHM.value)
    if algorithm_param is None:
        # invalid parameter
        logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))
        return BaseRsp(None, False, StandardMessageCode.E_100_9000_000004.get_formatted_msg(
            parameter_name=AlgorithmMetaDataParameter.ALGORITHM.value
        )).to_dict()

    data_fetcher_param = json.loads(request.data).get(AlgorithmMetaDataParameter.DATA_FETCHER.value)
    if data_fetcher_param is None:
        # invalid parameter
        logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))
        return BaseRsp(None, False, StandardMessageCode.E_100_9000_000004.get_formatted_msg(
            parameter_name=AlgorithmMetaDataParameter.DATA_FETCHER.value
        )).to_dict()

    # verify done, merge meta data
    data_wrapper = {
        AlgorithmMetaDataParameter.ALGORITHM.value: algorithm_param,
        AlgorithmMetaDataParameter.DATA_FETCHER.value: data_fetcher_param
    }

    # get real class
    from algorithm.algorithm_map import algorithm_map
    al_class = algorithm_map.get(al_id).get(AlgorithmMetaDataMap.JOB_CLS.value)

    if al_class is None:
        # target algorithm do not exist
        logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))
        return BaseRsp(None, False, StandardMessageCode.W_100_9000_100004.get_formatted_msg(
            algorithm_id=al_id
        )).to_dict()

    # get name
    _process_id = f'{al_id}-{get_current_date_time()}'
    # get instance
    exec(f'from {al_class.package_name} import {al_class.class_name}')
    _process_obj = eval(f'{al_class.class_name}(logger, '
                        f'{config_info_entity.sk_log_level}, '
                        f'db_connection, '
                        f'static_info.DATA_SOURCE_FLG, '
                        f'"{_process_id}", '
                        f'**data_wrapper )')
    process_pool.add_job(_process_obj)

    # log
    if config_info_entity.sk_log_level >= DebugLevel.LEVEL_2.value:
        logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
            program_name='main',
            pp_id=os.getppid(),
            l_id=os.getpid(),
        ))

    logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))

    rtn = BaseRsp(_process_id, True, None).to_dict()

    return rtn


@skate_app.route('/api/1/getPredictVal/<string:process_id>', methods=['POST'])
@swag_from('yaml/getPredictVal.yaml')
def get_predict_val(process_id):
    """
    get predict value by process id

    :param process_id: process id. This id is the return value of the declare_service() function

    :return: predicted value
    """
    global logger

    method_name = 'get_val'
    logger.info(StandardMessageCode.I_100_9000_200012.get_formatted_msg(method_name=method_name))

    # parse input data
    in_data = json.loads(request.data).get('data')
    if in_data is None:
        # TODO
        return BaseRsp(None, False, None).to_dict()
    else:
        # TODO
        logger.info(f'input data top 3 are: {in_data[:3]}')

    _tmp_p = process_pool.get_process_by_name(process_id)

    logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))

    in_data = np.array(in_data).reshape(-1, 1)
    rtn = BaseRsp(_tmp_p.predict(in_data), True, None).to_dict()

    return rtn


def init_env():
    """
    init environment
    """

    global config_info_entity, logger, db_connection, process_pool

    # log file =====
    _log_formatter = logging.Formatter(static_info.LOG_FORMAT_STR)
    _file_handler = logging.FileHandler('AiOps.log', mode='w', encoding='utf-8')
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
