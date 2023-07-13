# coding=utf-8
# author xin.he
import os
from multiprocessing import Lock, Process, Queue

import numpy as np

from skATE.algorithm.Al_IsolationForest import AlIsolationForest
from skATE.shares.message_code import StandardMessageCode
from skATE.shares.skate_enum import DebugLevel, AlgorithmMetaDataParameter
from skATE.skate_thread.skate_job import SkateJobTemplate1
from skATE.static_info import DataSourceEnum


class IsolationForestJob(SkateJobTemplate1):
    """
    Job for isolation forest
    """

    def __init__(self,
                 log,
                 log_level: int,
                 db_connection,
                 data_source_flg: DataSourceEnum = DataSourceEnum.MySQL,
                 name: str = '',
                 interval_second: int = 15,
                 **kwargs):
        """
        init

        :param log: logger object
        :param log_level: log level
        :param db_connection: database connection
        :param data_source_flg: data source type
        :param name: job name
        :param interval_second: interval second.
        :param kwargs: any other arguments
        """

        super().__init__(log, log_level, db_connection, data_source_flg, name, interval_second)

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
                program_name='IsolationForestJob',
                pp_id=os.getppid(),
                l_id=os.getpid(),
            ))

        # model object
        self._model = None
        # for sync model
        self._lock = Lock()

        # wrapper all data into a dict
        data_wrapper = {
            'data_source_flg': self._data_source_flg,
            'db_connection': self._db_connection,
        }
        data_wrapper.update(kwargs)

        # process
        self._process = Process(target=self.execute_job, args=(self._queue, data_wrapper, ))

    def train(self,
              q: Queue,
              data_wrapper):
        """
        train

        :param q: queue object(self._queue)
        :param data_wrapper: data wrapper
        """

        method_name = 'train'
        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(StandardMessageCode.I_100_9000_200012.get_formatted_msg(method_name=method_name))

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
                program_name='train',
                pp_id=os.getppid(),
                l_id=os.getpid(),
            ))

        ##########################
        # FOR AI MODEL
        ##########################

        algorithm_dict = data_wrapper.get(AlgorithmMetaDataParameter.ALGORITHM.value)
        data_fetcher_dict = data_wrapper.get(AlgorithmMetaDataParameter.DATA_FETCHER.value)

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(algorithm_dict)
            self._logger.info(data_fetcher_dict)

        # fetch data
        from skATE import static_info
        if data_wrapper.get('data_source_flg').value == static_info.DataSourceEnum.MySQL.value:
            # mysql
            from skATE.data_mysql.segment_latency_fetcher import SegmentLatencyFetcher
            fetcher = SegmentLatencyFetcher(data_wrapper.get('db_connection'),
                                            data_fetcher_dict.get('trace_name'),
                                            data_fetcher_dict.get('trace_id'),
                                            data_fetcher_dict.get('limitation'))
            # to avoid warning:
            # UserWarning: X does not have valid feature names, but <sk-learn class> was fitted with feature names
            fetched_rows = fetcher.fetch().values
            # revert
            fetched_rows = np.flip(fetched_rows)

            # GC
            del fetcher
        else:
            # TOD other database
            raise NotImplementedError()

        # algorithm model class
        _model_class = AlIsolationForest(
            n_estimators=algorithm_dict.get('n_estimators'),
            contamination=algorithm_dict.get('contamination'),
            max_features=algorithm_dict.get('max_features'),
            n_jobs=algorithm_dict.get('n_jobs'),
        )
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
            self._logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))

    def predict(self, in_data):
        """
        predict

        :param in_data: input data
        """

        method_name = 'predict'
        # log
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(StandardMessageCode.I_100_9000_200012.get_formatted_msg(method_name=method_name))

        # log
        if self._log_level >= DebugLevel.LEVEL_2.value:
            self._logger.info(StandardMessageCode.I_100_9000_200007.get_formatted_msg(
                program_name='predict',
                pp_id=os.getppid(),
                l_id=os.getpid(),
            ))

        rtn = []

        # verify
        if in_data is None:
            # log
            if self._log_level >= DebugLevel.LEVEL_1.value:
                self._logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))
            # input nothing return nothing
            return rtn

        # lock
        self._lock.acquire()
        try:
            # there is and only one model in queue
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
                    self._logger.warning(StandardMessageCode.W_100_9000_100005.get_formatted_msg())
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
            self._logger.info(StandardMessageCode.I_100_9000_200013.get_formatted_msg(method_name=method_name))

        return rtn.tolist()
