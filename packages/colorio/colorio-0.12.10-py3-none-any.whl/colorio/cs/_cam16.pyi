import numpy as np
from ..cat import cat16 as cat16
from ..illuminants import whitepoints_cie1931 as whitepoints_cie1931
from ._ciecam02 import compute_from as compute_from, compute_to as compute_to
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class CAM16:
    name: str
    c: Any
    N_c: Any
    F_L: Any
    n: Any
    z: Any
    N_bb: Any
    N_cb: Any
    A_w: Any
    h: Any
    e: Any
    H: Any
    def __init__(self, c: float, Y_b: float, L_A: float, whitepoint: ArrayLike = ...) -> None: ...
    def from_xyz100(self, xyz): ...
    def to_xyz100(self, data, description): ...

class CAM16UCS(ColorSpace):
    name: str
    labels: Any
    k0: int
    K_L: float
    c1: float
    c2: float
    cam16: Any
    def __init__(self, c: float, Y_b: float, L_A: float, whitepoint: ArrayLike = ...) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, jab: ArrayLike) -> np.ndarray: ...
