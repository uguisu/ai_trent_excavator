# coding=utf-8
# author xin.he

from absl import app
from absl import flags
from absl import logging

import shares

# ==========
# declare parameter
# ==========
FLAGS = flags.FLAGS
flags.DEFINE_string('bindingAddress', None, 'Binding address')
flags.DEFINE_string('bindingPort', None, 'Binding port')

flags.DEFINE_string('isAutoInstallPackage', None, 'Install required packages automatically.')

# ==========
# show logo
# ==========
shares.show_logo()

# ==========
# read config
# ==========
from config import load_config_file
config_info_entity = load_config_file()

# ==========
# make sure packages
# ==========
shares.make_sure_packages(config_info_entity)

# ==========
# main process
# ==========
import os
from cheroot.wsgi import PathInfoDispatcher, Server
from flask import Flask, request, Response

# declare application object
skate_app = Flask(__name__)
skate_app.config['SECRET_KEY'] = os.urandom(24)


def main(argv):
    # Unused.
    del argv

    init_env()

    # start http server
    server = Server((FLAGS.bindingAddress, int(FLAGS.bindingPort)),
                    PathInfoDispatcher({'/': skate_app}))

    logging.info(f'Server listening on {FLAGS.bindingAddress}:{FLAGS.bindingPort}')

    try:
        server.start()
    except KeyboardInterrupt:
        # release environment
        release_env()
        server.stop()


def init_env():
    """
    init environment
    """

    # log file =====
    # TODO https://stackoverflow.com/questions/59654893/python-absl-logging-without-timestamp-module-name
    logging.set_verbosity(logging.INFO)
    # _log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s() - %(levelname)s - %(message)s')
    # _file_handler = logging.FileHandler('./AiOps.log', mode='w', encoding='utf-8')
    # _file_handler.setFormatter(_log_formatter)
    # logger.addHandler(_file_handler)
    #
    # _console_handler = logging.StreamHandler()
    # _console_handler.setFormatter(_log_formatter)
    # logger.addHandler(_console_handler)

    pass


def release_env():
    """
    release environment
    """
    pass


if __name__ == '__main__':
    app.run(main)
