# coding=utf-8
# author xin.he

from skate_thread.skate_job import AbstractSkateJob


class MyTestSkateJob(AbstractSkateJob):
    """
    test class
    """

    def __init__(self,
                 name: str = '',
                 interval_second: int = 15):
        super().__init__(name, interval_second)

    def job_fn(self):
        """
        job function

        this method should be overwritten before execute
        """
        from datetime import datetime
        print(datetime.now().strftime("%Y%m%d%_H%M%S"))


def test_skate_job():

    name = 'my_test'
    interval_second = 11

    t = MyTestSkateJob(name=name, interval_second=interval_second)

    assert t.name == name
    assert t._interval_second == interval_second
