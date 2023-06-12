# coding=utf-8
# author xin.he
import logging
import time
import unittest

import static_info
from skate_thread.skate_job import AbstractSkateJob
from skate_thread.skate_process import ScheduledFixedProcessPool

# logger
logger = logging.getLogger('skATE')
logger.setLevel(logging.INFO)

_console_handler = logging.StreamHandler()
_log_formatter = logging.Formatter(static_info.LOG_FORMAT_STR)
_console_handler.setFormatter(_log_formatter)
logger.addHandler(_console_handler)


class MyTestSkateJob(AbstractSkateJob):
    """
    test class
    """

    def __init__(self,
                 name: str = '',
                 interval_second: int = 5):
        super().__init__(name, interval_second)

    def job_fn(self):
        """
        job function

        this method should be overwritten before execute
        """
        from shares.time_util import get_current_date_time
        print(get_current_date_time())

        # import time
        time.sleep(2)


class Test001(unittest.TestCase):

    def test_skate_job(self):

        name = 'my_test'
        interval_second = 11

        t = MyTestSkateJob(name=name, interval_second=interval_second)

        self.assertEqual(t.name, name)
        self.assertEqual(t._interval_second, interval_second)

    def test_skate_process(self):
        name = 'my_test'
        interval_second = 2

        t = MyTestSkateJob(name=name, interval_second=interval_second)

        process_pool = ScheduledFixedProcessPool(logger, pool_size=2)
        process_pool.add_job(t)

        # wait 10 seconds
        time.sleep(10)

        # stop process
        process_pool.stop_process_by_name(name)

        self.assertEqual(process_pool.job_amount, 0)


if __name__ == '__main__':
    unittest.main()
