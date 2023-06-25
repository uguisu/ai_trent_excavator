# coding=utf-8
# author xin.he
import time
from multiprocessing import Process, Queue


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

        # process
        self._process = Process(target=self.execute_job, args=(self._queue, ))

    def execute_job(self, q):
        """
        daemon job

        :param q: queue object(self._queue)
        """
        while not self.cancel_flg:
            # call train function
            self.train(q)
            # sleep
            time.sleep(self._interval_second)

    def train(self, q):
        """
        train

        this method should be overwritten before execute

        :param q: queue object(self._queue)
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
