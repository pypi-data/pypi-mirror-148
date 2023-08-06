from ._color_space import ColorSpace as ColorSpace
from ._hdr import HdrLinear as HdrLinear
from ._helpers import register as register
from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class ICtCp(ColorSpace):
    name: str
    labels: Any
    k0: int
    M1: Any
    m1: Any
    m2: Any
    c1: Any
    c2: Any
    c3: Any
    M2: Any
    def __init__(self) -> None: ...
    def from_rec2100(self, rgb: ArrayLike) -> ArrayLike: ...
    def to_rec2100(self, ictcp: ArrayLike) -> ArrayLike: ...
    def from_xyz100(self, xyz100: ArrayLike) -> ArrayLike: ...
    def to_xyz100(self, ictcp: ArrayLike) -> ArrayLike: ...
