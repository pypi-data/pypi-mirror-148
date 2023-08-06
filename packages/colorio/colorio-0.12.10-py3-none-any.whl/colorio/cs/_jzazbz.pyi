import numpy as np
from .._exceptions import ColorioError as ColorioError
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class JzAzBz(ColorSpace):
    name: str
    labels: Any
    k0: int
    b: float
    g: float
    c1: Any
    c2: Any
    c3: Any
    n: Any
    p: Any
    d: Any
    d0: float
    M1: Any
    M2: Any
    def __init__(self) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, jzazbz: ArrayLike) -> np.ndarray: ...
