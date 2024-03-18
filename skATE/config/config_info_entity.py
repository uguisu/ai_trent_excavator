# coding=utf-8
# author xin.he
from typing import Union


class ConfigInfo:
    """
    config file info
    """

    def __init__(self):
        """
        init
        """
        # [SECTION] dynamic-pip
        # proxy for install python packages dynamically
        self._dynamic_pip_proxy = None
        # install required packages automatically
        self._dynamic_pip_is_auto_install_package = None

        # [SECTION] http server
        # binding address
        self._http_binding_address = None
        # binding port
        self._http_binding_port = None

        # [SECTION] mysql
        # host
        self._mysql_host = None
        # port
        self._mysql_port = None
        # username
        self._mysql_username = None
        # password
        self._mysql_password = None
        # schema
        self._mysql_schema = None

        # [SECTION] elasticsearch
        # host
        self._es_host = None
        # port
        self._es_port = None
        # username
        self._es_username = None
        # password
        self._es_password = None

        # [SECTION] log_level
        # log level
        self._sk_log_level = None

        # [SECTION] neural_networks
        # is_dnn_enabled, a main settings of neural networks section.
        # Only by setting this option to True will the following content take effect
        self._neural_networks_is_dnn_enabled = None
        # User can use GPU to significantly improve the training performance
        self._neural_networks_is_gpu_enabled = None
        # when use CPU only, setup the proxy of network
        self._neural_networks_neural_networks_proxy = None
        # when use GPU, Nvidia CUDA 11.6 is required
        self._neural_networks_neural_networks_proxy_gpu = None

    @staticmethod
    def section_map() -> dict:
        """
        section and items map
        """
        return {
            'dynamic_pip': [
                'proxy',
                'is_auto_install_package',
            ],
            'http': [
                'binding_address',
                'binding_port',
            ],
            'mysql': [
                'host',
                'port',
                'username',
                'password',
                'schema',
            ],
            'es': [
                'host',
                'port',
                'username',
                'password',
            ],
            'sk_log': [
                'level',
            ],
            'neural_networks': [
                'is_dnn_enabled',
                'is_gpu_enabled',
                'neural_networks_proxy',
                'neural_networks_proxy_gpu',
            ],
        }

    @property
    def dynamic_pip_proxy(self) -> Union[None, str]:
        return self._dynamic_pip_proxy

    @dynamic_pip_proxy.setter
    def dynamic_pip_proxy(self, dynamic_pip_proxy):
        self._dynamic_pip_proxy = dynamic_pip_proxy

    @property
    def dynamic_pip_is_auto_install_package(self) -> Union[None, bool]:
        return self._dynamic_pip_is_auto_install_package

    @dynamic_pip_is_auto_install_package.setter
    def dynamic_pip_is_auto_install_package(self, dynamic_pip_is_auto_install_package):
        self._dynamic_pip_is_auto_install_package = eval(dynamic_pip_is_auto_install_package)

    @property
    def http_binding_address(self) -> Union[None, str]:
        return self._http_binding_address

    @http_binding_address.setter
    def http_binding_address(self, http_binding_address):
        self._http_binding_address = http_binding_address

    @property
    def http_binding_port(self) -> Union[None, int]:
        return self._http_binding_port

    @http_binding_port.setter
    def http_binding_port(self, http_binding_port):
        self._http_binding_port = int(http_binding_port)

    @property
    def mysql_host(self) -> Union[None, str]:
        return self._mysql_host

    @mysql_host.setter
    def mysql_host(self, mysql_host):
        self._mysql_host = mysql_host

    @property
    def mysql_port(self) -> Union[None, int]:
        return self._mysql_port

    @mysql_port.setter
    def mysql_port(self, mysql_port):
        if mysql_port is not None:
            self._mysql_port = int(mysql_port)

    @property
    def mysql_username(self) -> Union[None, str]:
        return self._mysql_username

    @mysql_username.setter
    def mysql_username(self, mysql_username):
        self._mysql_username = mysql_username

    @property
    def mysql_password(self) -> Union[None, str]:
        return self._mysql_password

    @mysql_password.setter
    def mysql_password(self, mysql_password):
        self._mysql_password = mysql_password

    @property
    def mysql_schema(self) -> Union[None, str]:
        return self._mysql_schema

    @mysql_schema.setter
    def mysql_schema(self, mysql_schema):
        self._mysql_schema = mysql_schema

    @property
    def es_host(self) -> Union[None, str]:
        return self._es_host

    @es_host.setter
    def es_host(self, es_host):
        self._es_host = es_host

    @property
    def es_port(self) -> Union[None, int]:
        return self._es_port

    @es_port.setter
    def es_port(self, es_port):
        if es_port is not None:
            self._es_port = int(es_port)

    @property
    def es_username(self) -> Union[None, str]:
        return self._es_username

    @es_username.setter
    def es_username(self, es_username):
        self._es_username = es_username

    @property
    def es_password(self) -> Union[None, str]:
        return self._es_password

    @es_password.setter
    def es_password(self, es_password):
        self._es_password = es_password

    @property
    def sk_log_level(self) -> Union[None, int]:
        return self._sk_log_level

    @sk_log_level.setter
    def sk_log_level(self, sk_log_level):
        self._sk_log_level = int(sk_log_level)

    @property
    def neural_networks_is_dnn_enabled(self) -> Union[None, bool]:
        return self._neural_networks_is_dnn_enabled

    @neural_networks_is_dnn_enabled.setter
    def neural_networks_is_dnn_enabled(self, neural_networks_is_dnn_enabled):
        self._neural_networks_is_dnn_enabled = eval(neural_networks_is_dnn_enabled)

    @property
    def neural_networks_is_gpu_enabled(self) -> Union[None, bool]:
        return self._neural_networks_is_gpu_enabled

    @neural_networks_is_gpu_enabled.setter
    def neural_networks_is_gpu_enabled(self, neural_networks_is_gpu_enabled):
        _wrk_neural_networks_is_gpu_enabled = None
        if neural_networks_is_gpu_enabled is not None:
            if isinstance(neural_networks_is_gpu_enabled, str):
                _wrk_neural_networks_is_gpu_enabled = eval(neural_networks_is_gpu_enabled)
            if isinstance(neural_networks_is_gpu_enabled, bool):
                _wrk_neural_networks_is_gpu_enabled = neural_networks_is_gpu_enabled
        self._neural_networks_is_gpu_enabled = _wrk_neural_networks_is_gpu_enabled

    @property
    def neural_networks_neural_networks_proxy(self) -> Union[None, str]:
        return self._neural_networks_neural_networks_proxy

    @neural_networks_neural_networks_proxy.setter
    def neural_networks_neural_networks_proxy(self, neural_networks_neural_networks_proxy):
        self._neural_networks_neural_networks_proxy = neural_networks_neural_networks_proxy

    @property
    def neural_networks_neural_networks_proxy_gpu(self) -> Union[None, str]:
        return self._neural_networks_neural_networks_proxy_gpu

    @neural_networks_neural_networks_proxy_gpu.setter
    def neural_networks_neural_networks_proxy_gpu(self, neural_networks_neural_networks_proxy_gpu):
        self._neural_networks_neural_networks_proxy_gpu = neural_networks_neural_networks_proxy_gpu
