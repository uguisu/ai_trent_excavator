# coding=utf-8
# author xin.he
import pymysql
import traceback

from config import ConfigInfo


class MySQLConnector:
    """
    MySQLConnector
    """
    def __init__(self, config_info_entity: ConfigInfo, logger=None):
        """
        init
        :param config_info_entity: ConfigInfo
        :param logger: logger
        """
        self._config_info_entity = config_info_entity
        self._logging = logger

    def open_db_connection(self):
        """
        Open database connection
        :return database connection object
        """
        try:
            con_rtn = pymysql.connect(host=self._config_info_entity.mysql_host,
                                      port=self._config_info_entity.mysql_port,
                                      database=self._config_info_entity.mysql_schema,
                                      user=self._config_info_entity.mysql_username,
                                      password=self._config_info_entity.mysql_password)

            return con_rtn
        except pymysql.err.OperationalError:
            if self._logging is not None:
                self._logging.error(traceback.format_exc())
            raise RuntimeError('MySQL connect failed.')
