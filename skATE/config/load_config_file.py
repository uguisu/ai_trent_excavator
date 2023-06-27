# coding=utf-8
# author xin.he
import configparser
import os

from skATE.config.config_info_entity import ConfigInfo
from skATE.shares.message_code import StandardMessageCode
from skATE.static_info import CONFIG_FILE_NAME


def load_config_file() -> ConfigInfo:
    """
    load config from file

    :return: an instance of ConfigInfo object
    """
    config_f = os.path.join(os.path.abspath(os.path.curdir), CONFIG_FILE_NAME)

    # reading file
    print(StandardMessageCode.I_100_9000_200006.get_formatted_msg(file_name=config_f))

    if not os.path.exists(config_f):
        # Can not find config file
        raise FileExistsError(StandardMessageCode.E_100_9000_000002.get_formatted_msg(cfg_file_name=CONFIG_FILE_NAME))

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

    if args.mysqlHost is not None:
        conf_info.mysql_host = args.mysqlHost
    if args.mysqlPort is not None:
        conf_info.mysql_port = args.mysqlPort
    if args.mysqlUsername is not None:
        conf_info.mysql_username = args.mysqlUsername
    if args.mysqlPassword is not None:
        conf_info.mysql_password = args.mysqlPassword
    if args.mysqlSchema is not None:
        conf_info.mysql_schema = args.mysqlSchema

    if args.esHost is not None:
        conf_info.es_host = args.esHost
    if args.esPort is not None:
        conf_info.es_port = args.esPort
    if args.esUsername is not None:
        conf_info.es_username = args.esUsername
    if args.esPassword is not None:
        conf_info.es_password = args.esPassword

    if args.skLogLevel is not None:
        conf_info.sk_log_level = args.skLogLevel

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
