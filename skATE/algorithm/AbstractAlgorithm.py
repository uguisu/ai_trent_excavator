# coding=utf-8
# author xin.he

class BaseAlgorithm:
    """
    Base Algorithm
    """

    def __init__(self):
        """
        init
        """
        # algorithm name
        self._name = ''

        # data (a pandas DataFrame for example)
        self._data = None
        # model
        self._model = None

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

    @property
    def model(self):
        """
        model
        """
        return self._model

    @model.setter
    def model(self, model):
        """
        setup model
        """
        self._model = model

    @property
    def data(self):
        """
        data
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        setup data
        """
        self._data = data

    def train(self):
        """
        train model

        this method should be overwritten before execute
        """
        raise NotImplementedError()

    def predict(self, **kwargs):
        """
        predict

        this method should be overwritten before execute
        """
        raise NotImplementedError()
