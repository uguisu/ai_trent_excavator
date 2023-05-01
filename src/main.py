# coding=utf-8
# author xin.he
import argparse
import logging

import shares
from config import load_config

# ============================================================
# declare parameter
# ============================================================
from config import args

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

# declare application object
skate_app = Flask(__name__)
skate_app.config['SECRET_KEY'] = os.urandom(24)


def init_env():
    """
    init environment
    """

    global config_info_entity, logger

    # log file =====
    _log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s() - %(levelname)s - %(message)s')
    _file_handler = logging.FileHandler('./AiOps.log', mode='w', encoding='utf-8')
    _file_handler.setFormatter(_log_formatter)
    logger.addHandler(_file_handler)

    _console_handler = logging.StreamHandler()
    _console_handler.setFormatter(_log_formatter)
    logger.addHandler(_console_handler)


def release_env():
    """
    release environment
    """
    pass


if __name__ == '__main__':

    init_env()

    # start http server
    server = Server((config_info_entity.http_binding_address, int(config_info_entity.http_binding_port)),
                    PathInfoDispatcher({'/': skate_app}))

    logger.info(f'Server listening on {config_info_entity.http_binding_address}'
                f':{config_info_entity.http_binding_port}')

    try:
        server.start()
    except KeyboardInterrupt:
        # release environment
        release_env()
        server.stop()
