import numpy as np
from ..illuminants import whitepoints_cie1931 as whitepoints_cie1931
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

def f(t): ...
def finv(t): ...

A: Any
Ainv: Any

class CIELAB(ColorSpace):
    name: str
    labels: Any
    k0: int
    whitepoint_xyz100: Any
    def __init__(self, whitepoint: ArrayLike = ...) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, lab: ArrayLike) -> np.ndarray: ...
