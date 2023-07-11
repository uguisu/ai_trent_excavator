# coding=utf-8
# author xin.he
from enum import Enum, unique, EnumMeta


# TODO later
# def convert_key_to_list(enum_class):
#     """
#     convert key to list
#
#     :param enum_class: enum class
#     """
#     # valid
#     assert enum_class is not None and isinstance(enum_class, EnumMeta)
#     return [x.value for x in list(enum_class)]


@unique
class DebugLevel(Enum):
    """
    debug level
    """
    # do not output debug info (default)
    LEVEL_0 = 0
    # only runtime info
    LEVEL_1 = 1
    # method or intermediate variable
    LEVEL_2 = 2
    # all debug info will be output
    LEVEL_3 = 3


@unique
class AlgorithmMetaDataMap(Enum):
    """
    Algorithm metadata map key name
    """
    # job class
    JOB_CLS = 'job'
    # algorithm class
    ALGORITHM_CLS = 'al'


@unique
class AlgorithmMetaDataParameter(Enum):
    """
    Algorithm metadata parameter key name

    Example: the target json format should be:
        {
            'algorithm': {
                'n_estimators': 100,
                'contamination': float(0.1),
                'max_features': float(1.0),
                'n_jobs': 2,
            },
            'data_fetcher': {
                'trace_name': '',
                'trace_id': '',
                'limitation': 2000,
            }
        }
    """
    # algorithm
    ALGORITHM = 'algorithm'
    # data fetcher
    DATA_FETCHER = 'data_fetcher'
