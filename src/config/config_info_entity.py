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
