# coding=utf-8
# author xin.he
from skATE.algorithm.AbstractAlgorithm import BaseAlgorithm


class AlIsolationForest(BaseAlgorithm):
    """
    IsolationForest

    Result: -1: abnormal; 1 normal;

    Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
    """

    def __init__(self,
                 n_estimators: int = 100,
                 contamination: float = float(0.1),
                 max_features: float = 1.0,
                 n_jobs: int = 2):
        """
        init

        :param n_estimators: The number of base estimators in the ensemble.
        :param contamination: ‘auto’ or float, default=‘auto’.
            The amount of contamination of the data set, i.e. the proportion of outliers in the data set.
        :param max_features: int or float, default=1.0
            The number of features to draw from X to train each base estimator.
        :param n_jobs: int, default=None
            The number of jobs to run in parallel for both fit and predict.
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

        from skATE.shares.message_code import StandardMessageCode

        # verify
        if self.data is None:
            # invalid parameter
            raise ValueError(StandardMessageCode.E_100_9000_000004.get_formatted_msg(parameter_name='data'))

        self.model.fit(self.data)

    # TODO useless?
    # def predict(self, **kwargs):
    #     """
    #     predict
    #
    #     :param kwargs: data for prediction
    #
    #     """
    #
    #     from skATE.shares.message_code import StandardMessageCode
    #
    #     # verify
    #     if kwargs is None:
    #         # invalid parameter
    #         raise ValueError(StandardMessageCode.E_100_9000_000004.get_formatted_msg(
    #             parameter_name='data for prediction'))
    #     if self.model is None:
    #         # train model before predict
    #         raise AttributeError(StandardMessageCode.E_100_9000_000003.get_formatted_msg())
    #
    #     return self.model.predict(kwargs['data'])

    @staticmethod
    def metadata() -> dict:
        """
        show metadata
        """
        return {
            'algorithm': {
                'n_estimators': 100,
                'contamination': float(0.1),
                'max_features': float(1.0),
                'n_jobs': 2,
            },
            'data_fetcher': AlIsolationForest.data_fetcher().metadata()
        }

    @staticmethod
    def data_fetcher():
        """
        get data fetcher class
        """
        from skATE.data_mysql.segment_latency_fetcher import SegmentLatencyFetcher
        return SegmentLatencyFetcher
