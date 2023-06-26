import os
import time
from multiprocessing import Lock

from shares.message_code import StandardMessageCode
from shares.skate_enum import DebugLevel
from shares.time_util import get_current_date_time
from skate_thread.skate_job import AbstractSkateJob


class Peppa(AbstractSkateJob):
    """
    test class
    """

    def __init__(self,
                 log,
                 log_level: int,
                 name: str = '',
                 interval_second: int = 15):
        """
        init

        :param log: logger object
        :param log_level: log level
        :param name: job name
        :param interval_second: interval second.
        """

        super().__init__(name, interval_second)

        self._logger = log
        self._log_level = log_level

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
                program_name='Peppa_init',
                pp_id=os.getppid(),
                l_id=os.getpid(),
            ))

        # model object
        self._model = None
        # for sync model
        self._lock = Lock()

    def predict(self, in_data):
        """
        predict

        :param in_data: input data
        """

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(f'get input data = {in_data}')

        rtn = []

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
                program_name='predict',
                pp_id=os.getppid(),
                l_id=os.getpid(),
            ))

        if in_data is None:
            # input nothing return nothing
            return rtn

        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(f'predicting.....')

        self._lock.acquire()
        try:
            if self._queue.qsize() == 1:
                self._model = self._queue.get()
            elif self._queue.qsize() > 1:
                raise RuntimeError()

            if self._model is None:

                # log
                if self._log_level >= DebugLevel.LEVEL_1.value:
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

        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(f'predicting..... done')

        return rtn

    def train(self, q):
        """
        train
        """

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
                program_name='train',
                pp_id=os.getppid(),
                l_id=os.getpid(),
            ))

        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
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

            # log
            if self._log_level >= DebugLevel.LEVEL_2.value:
                self._logger.info(f'put {dt} to queue')

        except Exception as e:
            self._logger.error(e)
        finally:
            self._lock.release()

        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(f'train finish')
