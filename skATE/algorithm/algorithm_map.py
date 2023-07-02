# coding=utf-8
# author xin.he


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
    "DEMO_001": AlgorithmMetaInfo('skate_thread.my_demo_job', 'Peppa'),
    'IsolationForest-001': AlgorithmMetaInfo('skate_thread.isolation_forest_job', 'IsolationForestJob'),
}
