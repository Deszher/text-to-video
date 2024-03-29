# pylint: skip-file
# -*- coding: utf-8 -*-
# File   : __init__.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 27/01/2018
#
# This file is part of Synchronized-BatchNorm-PyTorch.
# https://github.com/vacancy/Synchronized-BatchNorm-PyTorch
# Distributed under MIT License.

from .batchnorm import (  # noqa: F401
    SynchronizedBatchNorm1d,
    SynchronizedBatchNorm2d,
    SynchronizedBatchNorm3d,
)
from .replicate import (  # noqa: F401
    DataParallelWithCallback,
    patch_replication_callback,
)
