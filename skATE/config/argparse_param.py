# coding=utf-8
# author xin.he
import argparse


def declare_argparse():
    parser = argparse.ArgumentParser(description='AI Trent Excavator (skate)')
    parser.add_argument('--bindingAddress',
                        action='store',
                        dest='bindingAddress',
                        default=None,
                        help='Binding IP address')
    parser.add_argument('--bindingPort',
                        action='store',
                        dest='bindingPort',
                        default=None,
                        help='Binding Port')

    parser.add_argument('--proxy',
                        action='store',
                        dest='proxy',
                        default=None,
                        help='Proxy for install python packages dynamically')
    parser.add_argument('--isAutoInstallPackage',
                        action='store',
                        dest='isAutoInstallPackage',
                        default=None,
                        help='Install required packages automatically')

    parser.add_argument('--mysqlHost',
                        action='store',
                        dest='mysqlHost',
                        default=None,
                        help='Mysql Host')
    parser.add_argument('--mysqlPort',
                        action='store',
                        dest='mysqlPort',
                        default=None,
                        help='Mysql Port')
    parser.add_argument('--mysqlUsername',
                        action='store',
                        dest='mysqlUsername',
                        default=None,
                        help='Mysql User Name')
    parser.add_argument('--mysqlPassword',
                        action='store',
                        dest='mysqlPassword',
                        default=None,
                        help='Mysql Password')
    parser.add_argument('--mysqlSchema',
                        action='store',
                        dest='mysqlSchema',
                        default=None,
                        help='Mysql Schema')

    parser.add_argument('--esHost',
                        action='store',
                        dest='esHost',
                        default=None,
                        help='Elasticsearch Host')
    parser.add_argument('--esPort',
                        action='store',
                        dest='esPort',
                        default=None,
                        help='Elasticsearch Port')
    parser.add_argument('--esUsername',
                        action='store',
                        dest='esUsername',
                        default=None,
                        help='Elasticsearch User Name')
    parser.add_argument('--esPassword',
                        action='store',
                        dest='esPassword',
                        default=None,
                        help='Elasticsearch Password')

    parser.add_argument('--skLogLevel',
                        action='store',
                        dest='skLogLevel',
                        default=None,
                        help='Log level')

    return parser


args = declare_argparse().parse_args()
