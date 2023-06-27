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
