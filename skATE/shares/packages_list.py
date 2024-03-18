# coding=utf-8
# author xin.he
from skATE.config import ConfigInfo
from skATE.shares.message_code import StandardMessageCode

# all required packages
REQUIRED_PACKAGES = [
    # shares
    'numpy==1.24.3',
    # web server
    'Flask==2.2.3',
    'cheroot==9.0.0',
    'flasgger==0.9.7.1',
    'Werkzeug==2.2.2',
    # algorithm
    'scikit-learn==1.2.2',
    # data model
    'SQLAlchemy==2.0.15',
    'pandas==2.0.2',
    # mysql
    'PyMySQL==1.0.3',
    'cryptography==40.0.2',
    # Elasticsearch
    'elasticsearch==8.7.0'
]

DNN_PACKAGES_CPU_ONLY = [
    # pytorch
    'torch==1.13.1+cpu',
]

DNN_PACKAGES_GPU = [
    # pytorch
    'torch==1.13.1+cu116',
]


def make_sure_packages(config_info_entity: ConfigInfo, logger):
    """
    make sure all required packages are installed
    :param config_info_entity: an instance of ConfigInfo
    :param logger: logger
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

    d_pip.make_sure_packages(REQUIRED_PACKAGES)

    # install packages for neural network
    if config_info_entity.neural_networks_is_dnn_enabled is not None \
            and config_info_entity.neural_networks_is_dnn_enabled:

        if config_info_entity.neural_networks_is_gpu_enabled is not None \
                and config_info_entity.neural_networks_is_gpu_enabled:
            # use GPU
            d_pip.set_mirror_list([
                StaticResources.DEFAULT_PYPI_HOST,
            ])
            d_pip.extra_index_url = config_info_entity.neural_networks_neural_networks_proxy_gpu
            d_pip.make_sure_packages(DNN_PACKAGES_GPU)

            gpu_device_detection = False
            cuda_version = 'unknown'
            try:
                import torch
                # verify GPU device available
                gpu_device_detection = torch.cuda.is_available()
                cuda_version = torch.version.cuda
            except Exception as e:
                logger.error(e)
                # rollback default value
                gpu_device_detection = False
            finally:
                if config_info_entity.neural_networks_is_gpu_enabled != gpu_device_detection:
                    # GPU device not valid
                    logger.warning(StandardMessageCode.W_100_9000_100006.get_formatted_msg())
                else:
                    # log cuda info
                    logger.info(StandardMessageCode.I_100_9000_200014.get_formatted_msg(cuda_version=cuda_version))

            # override config info
            config_info_entity.neural_networks_is_gpu_enabled = gpu_device_detection
        else:
            # use CPU
            d_pip.set_mirror_list([
                StaticResources.DEFAULT_PYPI_HOST,
            ])
            d_pip.extra_index_url = config_info_entity.neural_networks_neural_networks_proxy
            d_pip.make_sure_packages(DNN_PACKAGES_CPU_ONLY)

    del d_pip
