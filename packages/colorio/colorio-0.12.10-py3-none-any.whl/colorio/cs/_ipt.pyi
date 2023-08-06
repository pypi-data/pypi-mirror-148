import numpy as np
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class IPT(ColorSpace):
    name: str
    labels: Any
    k0: int
    M1: Any
    M2: Any
    def __init__(self) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, ipt: ArrayLike) -> np.ndarray: ...
