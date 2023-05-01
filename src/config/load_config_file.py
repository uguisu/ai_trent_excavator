# coding=utf-8
# author xin.he
import configparser
import os

from config.config_info_entity import ConfigInfo
from static_info import CONFIG_FILE_NAME


def load_config_file() -> ConfigInfo:
    """
    load config from file

    :return: an instance of ConfigInfo object
    """
    config_f = os.path.join(os.path.abspath(os.path.curdir), CONFIG_FILE_NAME)
    print(f'Reading {config_f}')
    if not os.path.exists(config_f):
        raise FileExistsError(f'Can not find config file {CONFIG_FILE_NAME}.')

    config_file_reader = configparser.ConfigParser()
    config_file_reader.read(config_f)

    # declare ConfigInfo object
    rtn = ConfigInfo()
    # fetch & setup values
    for k in ConfigInfo.section_map().keys():
        for _item in ConfigInfo.section_map()[k]:
            try:
                exec(f'rtn.{k}_{_item} = config_file_reader["{k}"]["{_item}"]')
            except KeyError as e:
                # some values may do not exist
                exec(f'rtn.{k}_{_item} = None')

    del config_file_reader

    return rtn


def override_config_via_cli(args, conf_info: ConfigInfo) -> ConfigInfo:
    """
    override config info via command line parameter

    :param args: arguments
    :param conf_info: target ConfigInfo object
    :return: fixed ConfigInfo object
    """

    if args.bindingAddress is not None:
        conf_info.http_binding_address = args.bindingAddress

    if args.bindingPort is not None:
        conf_info.http_binding_port = args.bindingPort

    if args.proxy is not None:
        conf_info.dynamic_pip_proxy = args.proxy

    if args.isAutoInstallPackage is not None:
        conf_info.dynamic_pip_is_auto_install_package = args.isAutoInstallPackage

    return conf_info


def load_config(args) -> ConfigInfo:
    """
    load config

    :param args: system argument variables
    :return: an instance of ConfigInfo object
    """

    rtn = load_config_file()

    rtn = override_config_via_cli(args, rtn)

    return rtn
