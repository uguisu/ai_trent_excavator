# coding=utf-8
# author xin.he
import traceback

from sqlalchemy import create_engine

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
            con_rtn = create_engine(url=f'mysql+pymysql://{self._config_info_entity.mysql_username}:'
                                        f'{self._config_info_entity.mysql_password}@'
                                        f'{self._config_info_entity.mysql_host}:'
                                        f'{self._config_info_entity.mysql_port}/'
                                        f'{self._config_info_entity.mysql_schema}'
                                        f'?charset=utf8mb4',
                                    pool_size=5,
                                    max_overflow=0,
                                    pool_recycle=5*60,
                                    isolation_level="READ COMMITTED")
        except:
            # log error
            if self._logging is not None:
                self._logging.error(traceback.format_exc())
            from shares.message_code import StandardMessageCode
            # database connection failed
            raise RuntimeError(StandardMessageCode.E_100_9000_000001.get_formatted_msg(db='MySQL'))

        return con_rtn
