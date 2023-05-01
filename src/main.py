# coding=utf-8
# author xin.he
import argparse
import logging

import shares
from config import load_config_file, override_config_via_cli

# ==========
# declare parameter
# ==========
parser = argparse.ArgumentParser(description='AI Trent Excavator (skate)')
parser.add_argument('--bindingAddress',
                    action='store',
                    dest='bindingAddress',
                    default=None,
                    help='Binding IP address')
parser.add_argument('--bindingPort',
                    action='store',
                    dest='bindingPort',
                    default=None,
                    help='Binding Port')
parser.add_argument('--proxy',
                    action='store',
                    dest='proxy',
                    default=None,
                    help='Proxy for install python packages dynamically')
parser.add_argument('--isAutoInstallPackage',
                    action='store',
                    dest='isAutoInstallPackage',
                    default=None,
                    help='Install required packages automatically')

args = parser.parse_args()

# logger
logger = logging.getLogger('skai_analysis')
logger.setLevel(logging.INFO)

# ==========
# show logo
# ==========
shares.show_logo()

# ==========
# read config
# ==========
config_info_entity = load_config_file()
config_info_entity = override_config_via_cli(args, config_info_entity)

# ==========
# make sure packages
# ==========
shares.make_sure_packages(config_info_entity)

# ==========
# main process
# ==========
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
