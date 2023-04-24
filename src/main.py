# coding=utf-8
# author xin.he

# ==========
# show logo
# ==========
from shares import logo
print(logo)

# ==========
# make sure packages
# ==========
from dynamicPip import DynamicPip, StaticResources
from shares import REQUIRED_PACKAGES

d_pip = DynamicPip()
# for users who located in China main land
d_pip.set_mirror_list([
    StaticResources.DEFAULT_PYPI_HOST,
    'https://mirrors.aliyun.com/pypi/simple',
])
for req_pkg in REQUIRED_PACKAGES:
    d_pip.install_single_package(req_pkg)
del d_pip

# ==========
# main process
# ==========
import os
# import logging
from cheroot.wsgi import PathInfoDispatcher, Server
from flask import Flask, request, Response

from absl import app
from absl import flags
from absl import logging

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


# ==========
# declare parameter
# ==========
FLAGS = flags.FLAGS
flags.DEFINE_string('bindingAddress', '127.0.0.1', 'Binding address')
flags.DEFINE_string('bindingPort', '7821', 'Binding port')

if __name__ == '__main__':
    app.run(main)
