# coding=utf-8
# author xin.he

from skATE.shares.message_code import StandardMessageCode
from skATE.skate_thread.skate_job import AbstractSkateJob


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
        # pool valid flag
        self._is_pool_valid = True

    def add_job(self, job: AbstractSkateJob = None):
        """
        add job to thread pool

        :param job: AbstractSkateJob object
        """

        # verify
        if not self._is_pool_valid:
            # the thread pool is currently unavailable
            raise RuntimeError(StandardMessageCode.E_100_9000_000006.get_formatted_msg())

        if self._job_counter + 1 > self._pool_size:
            # too many jobs
            raise RuntimeError(StandardMessageCode.W_100_9000_100002.get_formatted_msg())

        # count job
        self._job_counter += 1

        if job.name is None or '' == job.name.strip():
            # generate a thread name
            from skATE.shares.time_util import get_current_date_time
            _name = f'job_{self._job_counter}_{get_current_date_time()}'
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
        # log process name
        self.log.info(StandardMessageCode.I_100_9000_200010.get_formatted_msg(job_name=process_name))

        proc_obj = self._job_dict.pop(process_name)
        proc_obj.process.kill()

    def get_process_by_name(self, process_name: str = '') -> AbstractSkateJob:
        """
        get process by name

        :param process_name: process name
        """
        # log process name
        self.log.info(StandardMessageCode.I_100_9000_200009.get_formatted_msg(job_name=process_name))

        proc_obj = self._job_dict.get(process_name)

        if proc_obj is None:
            # target job do not exist
            self.log.warn(StandardMessageCode.W_100_9000_100003.get_formatted_msg(job_name=process_name))

        return proc_obj

    def stop_all_process(self):
        """
        stop all jobs before close the process pool
        """
        # avoid add more jobs to current pool
        self._is_pool_valid = False
        # close all jobs
        for _k in self._job_dict.keys():
            self.stop_process_by_name(_k)

        # log
        self.log.info(StandardMessageCode.I_100_9000_200011.get_formatted_msg())

        del self._job_dict

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
