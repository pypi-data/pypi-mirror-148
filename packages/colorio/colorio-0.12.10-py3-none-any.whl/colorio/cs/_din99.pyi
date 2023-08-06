import numpy as np
from ._cielab import CIELAB as CIELAB
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class DIN99(ColorSpace):
    name: str
    labels: Any
    k0: int
    k_E: Any
    k_CH: Any
    cielab: Any
    p: Any
    sin_p2: Any
    cos_p2: Any
    sin_p6: Any
    cos_p6: Any
    def __init__(self, k_E: float = ..., k_CH: float = ..., variant: Union[str, None] = ...) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, lab99: ArrayLike) -> np.ndarray: ...
