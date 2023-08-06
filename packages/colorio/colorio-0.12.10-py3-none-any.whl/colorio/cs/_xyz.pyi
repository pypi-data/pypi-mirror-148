import numpy as np
from .._exceptions import ColorioError as ColorioError
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class XYZ(ColorSpace):
    name: str
    labels: Any
    k0: Any
    scaling: Any
    def __init__(self, scaling: float) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...

class XYZ1(XYZ):
    name: str
    def __init__(self) -> None: ...

class XYZ100(ColorSpace):
    name: str
    labels: Any
    def __init__(self) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
