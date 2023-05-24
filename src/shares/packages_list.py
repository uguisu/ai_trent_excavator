# coding=utf-8
# author xin.he
from config import ConfigInfo

# all required packages
REQUIRED_PACKAGES = [
    # shares
    'numpy==1.24.3',
    # web server
    'Flask==2.2.3',
    'cheroot==9.0.0',
    # algorithm
    'scikit-learn==1.2.2',
    # data model
    'SQLAlchemy==2.0.15',
    # mysql
    'PyMySQL==1.0.3',
    'cryptography==40.0.2',
    # Elasticsearch
    'elasticsearch==8.7.0'
]


def make_sure_packages(config_info_entity: ConfigInfo):
    """
    make sure all required packages are installed
    :param config_info_entity: an instance of ConfigInfo
    """

    # user can skip package install step
    if not config_info_entity.dynamic_pip_is_auto_install_package:
        # skip install
        return

    from dynamicPip import DynamicPip, StaticResources

    d_pip = DynamicPip()

    if config_info_entity.dynamic_pip_proxy is not None:
        # for users who want to use mirror
        d_pip.set_mirror_list([
            StaticResources.DEFAULT_PYPI_HOST,
            config_info_entity.dynamic_pip_proxy,
        ])

    for req_pkg in REQUIRED_PACKAGES:
        d_pip.install_single_package(req_pkg)
    del d_pip
