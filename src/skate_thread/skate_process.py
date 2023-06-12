# coding=utf-8
# author xin.he
from datetime import datetime

from shares.message_code import StandardMessageCode
from skate_thread.skate_job import AbstractSkateJob


class AbstractProcessPool:
    """
    Abstract Process Pool
    """
    def __init__(self, log):
        """
        init
        """

        # verify
        if log is None:
            # log object is required
            raise ValueError(StandardMessageCode.E_100_9000_000004.get_formatted_msg(parameter_name='log'))

        self._log = log

    @property
    def log(self):
        return self._log


class ScheduledFixedProcessPool(AbstractProcessPool):
    """
    Scheduled Fixed Process Pool
    """

    def __init__(self,
                 log,
                 pool_size: int = 10):

        super().__init__(log)

        # pool size
        self._pool_size = pool_size
        # current thread amount
        self._job_counter = 0
        # job dict. Key - job name; Val - job object
        self._job_dict = {}

    def add_job(self, job: AbstractSkateJob = None):
        """
        add job to thread pool

        :param job: AbstractSkateJob object
        """

        # verify
        if self._job_counter + 1 > self._pool_size:
            # too many jobs
            raise RuntimeError(StandardMessageCode.W_100_9000_100002.get_formatted_msg())

        # count job
        self._job_counter += 1

        if job.name is None or '' == job.name.strip():
            # generate a thread name
            _name = f'job_{self._job_counter}_{datetime.now().strftime("%Y%m%d%_H%M%S")}'
        else:
            _name = job.name

        # verify whether job name already exist
        if self._job_dict.get(_name) is not None:
            # the name already exist
            raise RuntimeError(StandardMessageCode.E_100_9000_000004.get_formatted_msg(parameter_name='job_name'))

        # log job name
        self.log.info(StandardMessageCode.I_100_9000_200008.get_formatted_msg(job_name=_name))

        self._job_dict[_name] = job

        # start job
        self._job_dict.get(_name).process.start()

        self.log.info(f'{_name} job started')

    def stop_process_by_name(self, process_name: str = ''):
        """
        stop process by name

        :param process_name: process name
        """

        print(f'stop {process_name}')

        proc_obj = self._job_dict.pop(process_name)
        proc_obj.process.kill()

    @property
    def job_amount(self) -> int:
        """
        current job amount
        """
        return len(self._job_dict)

    @property
    def pool_size(self) -> int:
        """
        pool size
        """
        return self._pool_size
