# coding=utf-8
# author xin.he
from typing import Iterator, Union

import pandas as pd
from pandas import DataFrame
from sqlalchemy.engine import Engine

from shares.message_code import StandardMessageCode


class IDataFetcher:
    """
    data fetcher interface

    child class should implement declare_sql() method
    """

    def __init__(self, database_connection):
        """
        init

        :param database_connection: database connection object
        """

        # verify
        assert database_connection is not None
        assert isinstance(database_connection, Engine)

        self._db_connect = database_connection
        self._sql = self.declare_sql()

    def fetch(self) -> Union[DataFrame, Iterator[DataFrame]]:
        """
        fetch data into pandas DataFrame
        """
        return pd.read_sql(self._sql, self._db_connect)

    def fetch_all_with_batch(self, chunk_size=10240) -> Union[DataFrame, Iterator[DataFrame]]:
        """
        fetch data into pandas DataFrame
        """
        return pd.read_sql(self._sql, self._db_connect, chunksize=chunk_size)

    def declare_sql(self) -> str:
        """
        declare SQL statement
        """

        raise NotImplementedError(StandardMessageCode.E_100_9000_000005.get_formatted_msg(method_name='declare_sql'))
