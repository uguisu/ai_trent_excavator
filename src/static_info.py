# coding=utf-8
# author xin.he
from enum import Enum, unique

__version__ = '0.0.1'

# config file name
CONFIG_FILE_NAME = r'skate_config.ini'

# log
LOG_FORMAT_STR = '%(asctime)s - %(name)s - %(funcName)s() - %(levelname)s - %(message)s'

# data source flag
@unique
class DataSourceEnum(Enum):
    """
    data source
    """
    ES = 1
    MySQL = 2


DATA_SOURCE_FLG: DataSourceEnum
