# coding=utf-8
# author xin.he
from algorithm.AbstractAlgorithm import BaseAlgorithm


class AlIsolationForest(BaseAlgorithm):
    """
    IsolationForest
    """

    def __init__(self,
                 n_estimators: int = 100,
                 contamination: float = float(0.1),
                 max_features: float = 1.0,
                 n_jobs: int = 2):
        """
        init
        """

        super().__init__()

        # setup name
        self.name = 'Isolation Forest'
        # init model
        self.init_model(n_estimators,
                        contamination,
                        max_features,
                        n_jobs)

    def init_model(self,
                   n_estimators,
                   contamination,
                   max_features,
                   n_jobs):
        """
        init model
        """
        from sklearn.ensemble import IsolationForest
        self.model = IsolationForest(n_estimators=n_estimators,
                                     max_samples='auto',
                                     contamination=contamination,
                                     max_features=max_features,
                                     n_jobs=n_jobs)

    def train(self):
        """
        train model
        """

        from shares.message_code import StandardMessageCode

        # verify
        if self.data is None:
            raise ValueError(StandardMessageCode.E_100_9000_000004.get_formatted_msg())

        self.model.fit(self.data)

    def predict(self, **kwargs):
        """
        predict

        :param kwargs: data for prediction

        """

        from shares.message_code import StandardMessageCode

        # verify
        if kwargs is None:
            raise ValueError(StandardMessageCode.E_100_9000_000004.get_formatted_msg())
        if self.model is None:
            raise AttributeError(StandardMessageCode.E_100_9000_000003.get_formatted_msg())

        return self.model.predict(kwargs['data'])
