# coding=utf-8
# author xin.he
from enum import Enum, unique

__version__ = '0.0.1'

# config file name
CONFIG_FILE_NAME = r'skate_config.ini'


# data source flag
@unique
class DataSourceEnum(Enum):
    """
    data source
    """
    ES = 1
    MySQL = 2


DATA_SOURCE_FLG: DataSourceEnum
