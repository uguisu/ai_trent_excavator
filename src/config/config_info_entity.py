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
            ]
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
