import numpy as np
from ..illuminants import whitepoints_cie1931 as whitepoints_cie1931
from ._cielab import f as f, finv as finv
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class CIELUV(ColorSpace):
    name: str
    labels: Any
    k0: int
    is_origin_well_defined: bool
    whitepoint_xyz100: Any
    un: Any
    vn: Any
    def __init__(self, whitepoint: ArrayLike = ...) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, luv: ArrayLike) -> np.ndarray: ...
