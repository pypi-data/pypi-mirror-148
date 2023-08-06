import numpy as np
from .._exceptions import ColorioError as ColorioError
from ..cat import cat02 as cat02
from ..illuminants import whitepoints_cie1931 as whitepoints_cie1931
from ._color_space import ColorSpace as ColorSpace
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

M_hpe: Any

def compute_from(rgb_, cs): ...
def compute_to(data, description, cs): ...

class CIECAM02:
    c: Any
    N_c: Any
    M: Any
    Minv: Any
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

class CAM02(ColorSpace):
    labels: Any
    k0: int
    ciecam02: Any
    name: Any
    def __init__(self, variant: str, c: float, Y_b: float, L_A: float, whitepoint: ArrayLike = ...) -> None: ...
    def from_xyz100(self, xyz: ArrayLike) -> np.ndarray: ...
    def to_xyz100(self, jab: ArrayLike) -> np.ndarray: ...

class CAM02LCD(CAM02):
    name: str
    def __init__(self, c, Y_b, L_A, whitepoint) -> None: ...

class CAM02SCD(CAM02):
    name: str
    def __init__(self, c, Y_b, L_A, whitepoint) -> None: ...

class CAM02UCS(CAM02):
    name: str
    def __init__(self, c, Y_b, L_A, whitepoint) -> None: ...
