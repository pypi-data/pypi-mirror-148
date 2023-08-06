import numpy as np
from ..illuminants import whitepoints_cie1931 as whitepoints_cie1931
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class PROLAB(ColorSpace):
    name: str
    labels: Any
    k0: int
    Q: Any
    q: Any
    Qinv: Any
    whitepoint_xyz100: Any
    whitepoint: Any
    def __init__(self, whitepoint=...) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, lab: ArrayLike) -> np.ndarray: ...
