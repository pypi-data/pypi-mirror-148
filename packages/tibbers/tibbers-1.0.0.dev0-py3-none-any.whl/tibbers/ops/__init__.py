import functools
import torch
import torch.nn as nn
import torch.nn.functional as F

from .conv import Conv1d, Conv2d, ConvTranspose2d
from .linear import Linear
from .pooling import MaxPool2d, AdaptiveAvgPool2d
from .dropout2d import Dropout2d
from .batchnorm import BatchNorm1d, BatchNorm2d
from .sparse import Embedding
from .normalization import LayerNorm
from .multiheadattention import MultiheadAttention
from .transformerencoderlayer import TransformerEncoderLayer


_OPS_MAP = {
    nn.Conv1d: Conv1d,
    nn.Conv2d: Conv2d,
    nn.ConvTranspose2d: ConvTranspose2d,
    nn.Linear: Linear,
    nn.MaxPool2d: MaxPool2d,
    nn.AdaptiveAvgPool2d: AdaptiveAvgPool2d,
    nn.Dropout2d: Dropout2d,
    nn.BatchNorm1d: BatchNorm1d,
    nn.BatchNorm2d: BatchNorm2d,
    nn.LayerNorm: LayerNorm,
    nn.Embedding: Embedding,
}

_HFTA_TORCH_IDENTICAL_OPS = {
    nn.Identity,
    nn.ReLU,
    nn.ReLU6,
    nn.Tanh,
    nn.LeakyReLU,
    nn.Dropout,
    nn.TransformerEncoder,
}


def convert_op(torch_op_class, B=1):
    if B > 0:
        if torch_op_class in _HFTA_TORCH_IDENTICAL_OPS:
            return torch_op_class
        else:
            return functools.partial(_OPS_MAP[torch_op_class], B=B)
    else:
        return torch_op_class


def convert_ops(B, *torch_op_classes):
    return (convert_op(op_class, B=B) for op_class in torch_op_classes)
