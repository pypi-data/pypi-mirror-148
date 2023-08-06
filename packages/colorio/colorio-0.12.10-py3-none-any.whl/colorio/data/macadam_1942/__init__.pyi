from ...cs import ColorSpace
from ..color_distance import ColorDistanceDataset as ColorDistanceDataset
from ..helpers import create_cs_class_instance as create_cs_class_instance
from typing import Any, Type

class MacAdam1942(ColorDistanceDataset):
    Y: Any
    whitepoint_xyz100: Any
    L_A: int
    c: float
    Y_b: int
    xy_centers: Any
    xy_offsets: Any
    def __init__(self, Y) -> None: ...
    def plot(self, cs_class: Type[ColorSpace], ellipse_scaling: float = ...): ...
