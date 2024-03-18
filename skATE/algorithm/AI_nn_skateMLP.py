# coding=utf-8
# author xin.he
import datetime
import time

import torch
import torch.nn.init as init
from torch import nn
from torch._C import device
from torch.utils.data import DataLoader

from skATE.algorithm.AbstractAlgorithm import BaseAlgorithm
from skATE.shares.message_code import StandardMessageCode
from skATE.shares.skate_enum import DebugLevel


class SkateMLP(nn.Module):
    """
    Declare Neural Networks - skATE MLP

    ┌─────────────┐
    │    Input    │
    └─────────────┘
           │
    ┌─────────────┐   ┐
    │    Linear   │   ┆
    ├─────────────┤   ┆
    │  LayerNorm  │   ┆ * 6 (times)
    ├─────────────┤   ┆
    │    Tanh     │   ┆
    └─────────────┘   ┘
           │
    ┌─────────────┐
    │   Output    │
    └─────────────┘
    """

    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int):
        """
        init

        :param in_dim: input dimension
        :param hidden_dim: hidden dimension
        :param out_dim: output dimension
        """

        super(SkateMLP, self).__init__()

        self.l1 = nn.Linear(in_dim, hidden_dim, dtype=torch.float32)
        self.l2 = nn.Linear(hidden_dim, hidden_dim * 2, dtype=torch.float32)
        self.l3 = nn.Linear(hidden_dim * 2, hidden_dim * 2, dtype=torch.float32)
        self.l4 = nn.Linear(hidden_dim * 2, hidden_dim, dtype=torch.float32)
        self.l5 = nn.Linear(hidden_dim, int(hidden_dim / 2), dtype=torch.float32)
        self.l6 = nn.Linear(int(hidden_dim / 2), out_dim, dtype=torch.float32)

        self.tanh = nn.Tanh()

        self.ly_norm1 = nn.LayerNorm(hidden_dim)
        self.ly_norm2 = nn.LayerNorm(hidden_dim * 2)
        self.ly_norm3 = nn.LayerNorm(hidden_dim * 2)
        self.ly_norm4 = nn.LayerNorm(hidden_dim)
        self.ly_norm5 = nn.LayerNorm(int(hidden_dim / 2))
        self.ly_norm6 = nn.LayerNorm(out_dim)

        # Custom weight initialization
        self.apply(SkateMLP.weight_init)

    def forward(self, x):
        """
        forward
        """
        rtn = self.tanh(self.ly_norm1(self.l1(x)))
        rtn = self.tanh(self.ly_norm2(self.l2(rtn)))
        rtn = self.tanh(self.ly_norm3(self.l3(rtn)))
        rtn = self.tanh(self.ly_norm4(self.l4(rtn)))
        rtn = self.tanh(self.ly_norm5(self.l5(rtn)))
        rtn = self.tanh(self.ly_norm6(self.l6(rtn)))

        return rtn

    @staticmethod
    def weight_init(m):
        """
        Custom weight initialization
        """
        if isinstance(m, nn.Linear):
            init.xavier_uniform_(m.weight)
        # if isinstance(m, nn.LayerNorm):
        #     init.zeros_(m.weight)


def detect_accelerators() -> device:
    """
    detect available accelerators(GPU / CPU)
    """
    # find useful device
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def show_model_info(tgt_model):
    """
    show model info
    :param tgt_model: model object
    """

    def calculate_parameter_number():
        total_num = sum(p.numel() for p in tgt_model.parameters())
        trainable_num = sum(p.numel() for p in tgt_model.parameters() if p.requires_grad)
        return f'Total: {total_num:,} | Trainable: {trainable_num:,}'

    rtn = (f'\n'
           f'==================================== Model Info ====================================\n'
           f''
           f'Model Architecture:\n'
           f'------------------------------------------------------------------------------------\n'
           f'{tgt_model}\n'
           f'------------------------------------------------------------------------------------\n'
           f'{calculate_parameter_number()}\n'
           f'====================================================================================\n')

    return rtn


class AlNnSkateMLP(BaseAlgorithm):
    """
    Neural Networks - skATE MLP

    Result: predict value
    """

    def __init__(self,
                 log,
                 log_level: int,
                 in_dim: int,
                 hidden_dim: int,
                 out_dim: int,
                 epoch: int = 100):
        """
        init

        BaseAlgorithm.data should be a `torch.utils.data.Dataset` object

        :param log: logger object
        :param log_level: log level
        :param in_dim: input dimension
        :param hidden_dim: hidden dimension
        :param out_dim: output dimension
        :param epoch: epoch
        """

        super(AlNnSkateMLP, self).__init__()

        # setup name
        self.name = 'skATE MLP'
        # log
        self._logger = log
        # log level
        self._log_level = log_level
        # device
        self.device = detect_accelerators()
        # log device
        if self._log_level >= DebugLevel.LEVEL_1.value:
            self._logger.info(StandardMessageCode.I_100_9000_200015.get_formatted_msg(device=self.device))

        # hyper-parameters
        self.epoch = epoch
        self.batch_size = 32
        self.training_proportion = 0.8
        self.lr = 0.0001
        self.in_dim = in_dim
        self.hidden_dim = hidden_dim
        self.out_dim = out_dim

        # init model
        self.init_model()

    def init_model(self):
        """
        init model
        """

        self.model = SkateMLP(self.in_dim, self.hidden_dim, self.out_dim)
        self.model.to(device=self.device)
        # log model
        if self._log_level >= DebugLevel.LEVEL_3.value:
            self._logger.info(show_model_info(self.model))

    def run_epoch(self,
                  train_data_iter,
                  model,
                  optimizer,
                  loss_fn):
        """
        Train a single epoch
        """

        loss_train = 0.0

        for i, batch in enumerate(train_data_iter):
            train_features, train_labels = batch
            train_features = train_features.to(device=self.device)
            train_labels = train_labels.to(device=self.device)
            wrk_train_labels = train_labels.view(-1, 1)

            outputs = model(train_features)

            # loss will return a tensor
            loss = loss_fn(outputs, wrk_train_labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            loss_train = loss.item()

        return loss_train

    def train(self):
        """
        train model
        """
        # load all data and split into train/test groups
        all_data_len = len(self.data)
        train_size = int(all_data_len * self.training_proportion)
        test_size = all_data_len - train_size
        training_data, test_data = torch.utils.data.random_split(self.data, [train_size, test_size])

        train_dataloader = DataLoader(training_data, batch_size=self.batch_size, shuffle=True)
        test_dataloader = DataLoader(test_data, batch_size=self.batch_size, shuffle=True)

        # declare optimizer
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        # loss function
        loss_fn = nn.MSELoss()

        # mark start time
        start = time.time()

        loss_train = 0.0

        for i in range(self.epoch):

            # turn into training status
            self.model.train()

            _loss = self.run_epoch(
                train_dataloader,
                self.model,
                optimizer,
                loss_fn,
            )

            loss_train = _loss

            if i % 10 == 0:
                # get lr
                lr = optimizer.param_groups[0]["lr"]
                # calculate elapsed time
                elapsed = time.time() - start

                if self._log_level >= DebugLevel.LEVEL_2.value:
                    self._logger.info(
                        f'{datetime.datetime.now():%Y/%m/%d %H:%M:%S} | Epoch Step: {i:>6} | '
                        f'Loss: {_loss:12.6f} | Learning Rate: {lr:6.1e} | Elapsed time: {elapsed}'
                    )

                # test
                self.model.eval()
                with torch.no_grad():

                    # ====== Use Test Data ======
                    test_loss = torch.zeros(1, device=self.device, dtype=torch.float32)

                    for _, batch in enumerate(test_dataloader):
                        test_features, test_labels = batch
                        test_features = test_features.to(device=self.device)
                        test_labels = test_labels.to(device=self.device)
                        wrk_test_labels = test_labels.view(-1, 1)

                        test_outputs = self.model(test_features)
                        # calculate loss manually
                        test_loss += torch.sum(wrk_test_labels - test_outputs, dim=0)

                    avg_test_loss = test_loss / test_size

                    if self._log_level >= DebugLevel.LEVEL_2.value:
                        self._logger.info(
                            f'{datetime.datetime.now():%Y/%m/%d %H:%M:%S} | Test Loss: {avg_test_loss.item():12.6f}'
                        )

                start = time.time()

        # TODO use test average loss
        # print(
        #     f'{datetime.datetime.now():%Y/%m/%d %H:%M:%S} | Epoch Step:  Final | '
        #     f'Loss: {loss_train} | Learning Rate: {lr:6.1e}'
        # )

    @staticmethod
    def metadata() -> dict:
        """
        show metadata
        """
        # TODO
        pass

    @staticmethod
    def data_fetcher():
        """
        get data fetcher class
        """
        # TODO
        pass
