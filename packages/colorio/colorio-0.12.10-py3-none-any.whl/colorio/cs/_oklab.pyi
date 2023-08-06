import numpy as np
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class OKLAB(ColorSpace):
    name: str
    labels: Any
    k0: int
    M1: Any
    M1inv: Any
    M2: Any
    M2inv: Any
    lightness_type: Any
    k1: float
    k2: float
    k3: Any
    def __init__(self, lightness_type: str = ...) -> None: ...
    def from_xyz100(self, xyz100: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, lab: ArrayLike) -> np.ndarray: ...
