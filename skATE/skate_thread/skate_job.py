# coding=utf-8
# author xin.he
import time
from multiprocessing import Queue

from skATE.static_info import DataSourceEnum


class AbstractSkateJob:
    """
    abstract skate job object
    """

    def __init__(self,
                 name: str = '',
                 interval_second: int = 15):
        """
        init

        :param name: job name
        :param interval_second: interval second.
        """

        self._name = name
        self._interval_second = interval_second
        # process cancel flag
        self._cancel_flg = False
        # sync trained model
        self._queue = Queue()

        # process should be started in subclass.
        # refer following example
        # self._process = Process(target=self.execute_job, args=(self._queue, xxxxxxx))

    def execute_job(self,
                    q: Queue,
                    data_wrapper):
        """
        daemon job

        :param q: queue object(self._queue)
        :param data_wrapper: data wrapper
        """
        while not self.cancel_flg:
            # call train function
            self.train(q, data_wrapper)
            # sleep
            time.sleep(self._interval_second)

    def train(self,
              q: Queue,
              data_wrapper):
        """
        train

        this method should be overwritten before execute

        :param q: queue object(self._queue)
        :param data_wrapper: data wrapper
        """
        raise NotImplementedError()

    def predict(self, in_data):
        """
        predict

        this method should be overwritten before execute

        :param in_data: input data
        """
        raise NotImplementedError()

    @property
    def cancel_flg(self) -> bool:
        return self._cancel_flg

    @cancel_flg.setter
    def cancel_flg(self, cancel_flg: bool):
        self._cancel_flg = cancel_flg

    @property
    def name(self) -> str:
        """
        name
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        setup algorithm name
        """
        self._name = name

    @property
    def process(self):
        """
        process
        """
        return self._process


class SkateJobTemplate1(AbstractSkateJob):
    """
    job template 1
    """

    def __init__(self,
                 log,
                 log_level: int,
                 db_connection,
                 data_source_flg: DataSourceEnum = DataSourceEnum.MySQL,
                 name: str = '',
                 interval_second: int = 15):
        """
        init

        :param log: logger object
        :param log_level: log level
        :param db_connection: database connection
        :param data_source_flg: data source type
        :param name: job name
        :param interval_second: interval second.
        """

        super().__init__(name, interval_second)

        self._logger = log
        self._log_level = log_level
        self._db_connection = db_connection
        self._data_source_flg = data_source_flg
