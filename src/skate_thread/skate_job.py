# coding=utf-8
# author xin.he


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
        # thread cancel flag
        self._cancel_flg = False

    def execute_job(self):
        """
        start job
        """

        # call job function
        self.job_fn()

        if not self.cancel_flg:
            import threading
            threading.Timer(self._interval_second, self.execute_job()).start()

    def job_fn(self):
        """
        job function

        this method should be overwritten before execute
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
