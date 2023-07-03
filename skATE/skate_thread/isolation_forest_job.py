# coding=utf-8
# author xin.he
import os
from multiprocessing import Lock, Process, Queue

from skATE.algorithm.Al_IsolationForest import AlIsolationForest
from skATE.shares.message_code import StandardMessageCode
from skATE.shares.skate_enum import DebugLevel
from skATE.skate_thread.skate_job import AbstractSkateJob
from skATE.static_info import DataSourceEnum


class IsolationForestJob(AbstractSkateJob):
    """
    Job for isolation forest
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

        meta_data = {
            'data_source_flg': self._data_source_flg,
            'db_connection': self._db_connection,
        }

        # process
        self._process = Process(target=self.execute_job, args=(self._queue, meta_data, ))

    def train(self,
              q: Queue,
              meta_data):
        """
        train

        :param q: queue object(self._queue)
        :param meta_data: meta data
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

        ##########################
        # FOR AI MODEL
        ##########################

        # TODO
        trace_name = 'mall|happysk|'
        trace_id = 'bWFsbHxoYXBweXNrfA==.2'
        limitation = 2000

        # fetch data
        from skATE import static_info
        if meta_data.get('data_source_flg').value == static_info.DataSourceEnum.MySQL.value:
            # mysql
            from skATE.data_mysql.segment_latency_fetcher import SegmentLatencyFetcher
            fetcher = SegmentLatencyFetcher(meta_data.get('db_connection'),
                                            trace_name,
                                            trace_id,
                                            limitation)
            # to avoid warning:
            # UserWarning: X does not have valid feature names, but <sk-learn class> was fitted with feature names
            fetched_rows = fetcher.fetch().values

            # GC
            del fetcher
        else:
            # TOD other database
            raise NotImplementedError()


        # TODO add some meta data for model class
        # algorithm model class
        _model_class = AlIsolationForest()
        _model_class.data = fetched_rows
        _model_class.train()

        # update model
        self._lock.acquire()
        try:
            # remove all older model
            while not q.empty():
                _to_del = q.get()
                del _to_del

            q.put(_model_class.model)

        except Exception as e:
            self._logger.error(e)
        finally:
            self._lock.release()

        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(f'train finish')

    def predict(self, in_data):
        """
        predict

        :param in_data: input data
        """

        rtn = []

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
                program_name='predict',
                pp_id=os.getppid(),
                l_id=os.getpid(),
            ))

        # verify
        if in_data is None:
            # input nothing return nothing
            return rtn

        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(f'predicting.....')

        self._lock.acquire()
        try:
            if self._queue.qsize() == 1:
                # remove old model
                del self._model
                # pop-up model object from Queue
                self._model = self._queue.get()
            elif self._queue.qsize() > 1:
                raise RuntimeError()

            if self._model is None:

                # log
                if self._log_level >= DebugLevel.LEVEL_1.value:
                    self._logger.info(f'model is none')

                # model has not been trained yet
                return []

            rtn = self._model.predict(in_data)

        except Exception as e:
            # raise e
            self._logger.error(e)
        finally:
            self._lock.release()

        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(f'predicting..... done')

        return rtn.tolist()
