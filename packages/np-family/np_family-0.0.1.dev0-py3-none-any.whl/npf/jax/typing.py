from typing import (
    Union,
    Optional,
    Tuple,
    List,
    Sequence,
    Any,
    Callable,
)

from jax.numpy import DeviceArray


#! TODO: temporary wrapper
class Array(type):
    def __class_getitem__(cls, *args):
        return DeviceArray


class TensorDim(str):
    def __new__(cls, name):
        return super().__new__(cls, name)

    def __eq__(self, other):
        return str(self) == str(other)

    def __add__(self, other):
        return TensorDim(f"{self} + {other}")

    def __mul__(self, other):
        return TensorDim(f"{self} * {other}")

    def __hash__(self):
        return str.__hash__(self)


B = TensorDim("batch")
C = TensorDim("context")
D = TensorDim("discrete")
K = TensorDim("key_dim")
L = TensorDim("latent")
M = TensorDim("M")
N = TensorDim("N")
T = TensorDim("target")
P = TensorDim("point")
Q = TensorDim("query_dim")
R = TensorDim("r_dim")
S = TensorDim("source")
V = TensorDim("value_dim")
X = TensorDim("x_dim")
Y = TensorDim("y_dim")
Z = TensorDim("z_dim")
G = TensorDim("generate number")

QK = TensorDim("query_key_dim")
