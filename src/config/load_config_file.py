# coding=utf-8
# author xin.he
import configparser
import os

from config.config_info_entity import ConfigInfo
from static_info import CONFIG_FILE_NAME


def load_config_file() -> ConfigInfo:
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
