# coding=utf-8
# author xin.he
import logging
import unittest

import numpy as np
import torch
from torch.utils.data import Dataset

from skATE import static_info
from skATE.algorithm.AI_nn_skateMLP import SkateMLP

# logger
logger = logging.getLogger('skATE')
logger.setLevel(logging.INFO)

_console_handler = logging.StreamHandler()
_log_formatter = logging.Formatter(static_info.LOG_FORMAT_STR)
_console_handler.setFormatter(_log_formatter)
logger.addHandler(_console_handler)


class SkateRandomDataSet(Dataset):

    def __init__(self, data_size: int = 100):
        """
        init

        y = sin() + cos() + bias
        """

        super(SkateRandomDataSet).__init__()

        self.data_size = data_size

        self.feature1 = np.sin(np.array([i * np.pi / 180 for i in range(self.data_size)]))
        self.feature2 = np.cos(np.array([i * np.pi / 180 for i in range(self.data_size)]))

        # generate label
        self.label = self.feature1 + self.feature2

        # bias
        _bias = np.random.uniform(low=-0.5, high=0.5, size=self.data_size)
        # adjust feature1
        self.feature1 = self.feature1 + _bias

        # another bias
        _bias = np.random.uniform(low=-0.5, high=0.5, size=self.data_size)
        # adjust feature2
        self.feature2 = self.feature2 + _bias

        # construct data
        self.data = np.stack((self.feature1, self.feature2, self.label), axis=-1)
        self.data = self.data.astype(np.float32)

        self.data_shape_row, self.data_shape_col = self.data.shape

        # print(f'row = {self.data_shape_row}; col = {self.data_shape_col}')

    def __getitem__(self, idx):
        _sub_data = self.data[idx]
        # data, label
        return _sub_data[:self.data_shape_col - 1], _sub_data[-1:]

    def __len__(self):
        return self.data_shape_row


class TestSkateMLP001(unittest.TestCase):

    def test_make_model_001(self):
        """
        test make model
        """

        in_dim = 3
        hidden_dim = 5
        out_dim = 1

        model = SkateMLP(in_dim, hidden_dim, out_dim)

        one_tensor = torch.ones(in_dim, dtype=torch.float32)

        out_val = model(one_tensor)

        self.assertEqual(out_dim, out_val.shape[0])

    def test_detect_accelerators(self):
        """
        function: detect_accelerators()
        """

        from skATE.algorithm.AI_nn_skateMLP import detect_accelerators

        self.assertTrue(str(detect_accelerators()) in ['cuda', 'cpu'])

    def test_train_model(self):
        """
        train model
        """
        from skATE.algorithm.AI_nn_skateMLP import AlNnSkateMLP
        from skATE.shares.skate_enum import DebugLevel

        in_dim = 2
        hidden_dim = 8
        out_dim = 1
        epoch = 20

        al_obj = AlNnSkateMLP(logger, DebugLevel.LEVEL_3.value, in_dim, hidden_dim, out_dim, epoch)
        al_obj.data = SkateRandomDataSet()
        al_obj.train()


if __name__ == '__main__':
    unittest.main()
