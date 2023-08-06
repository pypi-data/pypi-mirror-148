import numpy as np
from ..illuminants import whitepoints_cie1931 as whitepoints_cie1931
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class RLAB(ColorSpace):
    name: str
    labels: Any
    k0: int
    whitepoint: Any
    sigma: Any
    A: Any
    Ainv: Any
    def __init__(self, Y_n: float = ..., D: float = ..., whitepoint: ArrayLike = ..., sigma: float = ...) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, lab: ArrayLike) -> np.ndarray: ...
