# coding=utf-8
# author xin.he
from skATE.shares.skate_enum import AlgorithmMetaDataMap


class AlgorithmMetaInfo:
    """
    Algorithm Meta Info
    """

    def __init__(self,
                 package_name: str = '',
                 class_name: str = ''):
        """
        init

        :param package_name: package name
        :param class_name: class name
        """

        self._pkg = package_name
        self._cls = class_name

    @property
    def package_name(self) -> str:
        return self._pkg

    @property
    def class_name(self) -> str:
        return self._cls


# algorithm class meta info
algorithm_map = {
    'IsolationForest-001': {
        AlgorithmMetaDataMap.JOB_CLS.value:
            AlgorithmMetaInfo('skate_thread.isolation_forest_job', 'IsolationForestJob'),
        AlgorithmMetaDataMap.ALGORITHM_CLS.value:
            AlgorithmMetaInfo('skATE.algorithm.Al_IsolationForest', 'AlIsolationForest'),
    }
}
