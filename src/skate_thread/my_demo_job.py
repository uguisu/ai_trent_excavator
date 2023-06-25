import os
import time
from multiprocessing import Lock

from shares.time_util import get_current_date_time
from skate_thread.skate_job import AbstractSkateJob


class Peppa(AbstractSkateJob):
    """
    test class
    """

    def __init__(self,
                 log,
                 name: str = '',
                 interval_second: int = 15):
        """
        init

        :param log: logger object
        :param name: job name
        :param interval_second: interval second.
        """

        super().__init__(name, interval_second)

        # self._queue = queue
        self._logger = log

        # self._logger.info(f'from Peppa init name: {__name__}')
        self._logger.info(f'from Peppa init parent process id: {os.getppid()}')
        self._logger.info(f'from Peppa init process id: {os.getpid()}')

        # model object
        self._model = None

        self._lock = Lock()

    def predict(self, in_data):
        """
        predict

        :param in_data: input data
        """

        self._logger.info(f'get input data = {in_data}')

        rtn = []

        # self._logger.info(f'from predict name: {__name__}')
        self._logger.info(f'from predict parent process id: {os.getppid()}')
        self._logger.info(f'from predict process id: {os.getpid()}')


        if in_data is None:
            # input nothing return nothing
            return rtn


        self._logger.info(f'predicting.....')
        self._lock.acquire()
        try:
            if self._queue.qsize() == 1:
                self._model = self._queue.get()
            elif self._queue.qsize() > 1:
                raise RuntimeError()

            if self._model is None:
                self._logger.info(f'model is none')
                # model has not been trained yet
                return [-255, -255, -255, -255]

            # success!!!
            self._logger.info(f'self._model = {self._model}')

            rtn = [self._model]

            time.sleep(1)
        except Exception as e:
            # raise e
            self._logger.error(e)
        finally:
            self._lock.release()
        self._logger.info(f'predicting..... done')

        return rtn

    def train(self, q):
        """
        train
        """

        # self._logger.info(f'from train name: {__name__}')
        self._logger.info(f'from train parent process id: {os.getppid()}')
        self._logger.info(f'from train process id: {os.getpid()}')

        self._logger.info(f'train start')
        dt = get_current_date_time()

        # dummy training
        time.sleep(5)

        # update model
        self._lock.acquire()
        try:
            # remove all older model
            while not q.empty():
                q.get()

            q.put(dt)
            self._logger.info(f'put {dt} to queue')

        except Exception as e:
            self._logger.error(e)
        finally:
            self._lock.release()

        self._logger.info(f'train finish')
