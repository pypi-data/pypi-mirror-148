#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : aizoo.
# @File         : losses
# @Time         : 2022/4/25 下午3:48
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : criterion


import torch
from torch import nn
from torch.nn import functional as F

from aizoo import epsilon


class F1Loss(nn.Module):  # nn.CrossEntropyLoss
    """
    函数光滑化杂谈：不可导函数的可导逼近
    https://spaces.ac.cn/archives/6620
    直接优化指标只是一个途径，但它未必是最好的途径，通常来说只是用于后期微调，前期还是用交叉熵居多。
    """

    def __init__(self):
        super().__init__()

    def forward(self, y_true, y_pred):
        """todo 多分类

        @param y_true: 注意维度
        @param y_pred: 正类概率（softmax后的结果）
        @return:
        """

        loss = 2 * (y_true * y_pred).sum() / ((y_true + y_pred).sum() + epsilon)
        return - loss


class AccuracyLoss(nn.Module):
    """
    a = torch.randn(100, 2, requires_grad=True).softmax(dim=1)
    b = torch.empty(100, dtype=torch.long).random_(2)

    (a.argmax(1) == b).sum()
    (a * torch.nn.functional.one_hot(b)).sum()
    """

    def __init__(self, batch_size=1):
        super().__init__()
        self.batch_size = batch_size

    def forward(self, y_true, y_pred):
        loss = (F.one_hot(y_true) * y_pred).sum() / self.batch_size
        return - loss


class DiceLoss(nn.Module):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    n = 5
    y_pred = torch.randn(n, 1)
    y_true = torch.empty(n, dtype=torch.long).random_(5)

    print(F1Loss()(y_true, y_pred))
