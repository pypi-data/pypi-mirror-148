from ...cs import ColorSpace
from ..color_distance import ColorDistanceDataset as ColorDistanceDataset
from ..helpers import create_cs_class_instance as create_cs_class_instance
from typing import Any, Type

class MacAdam1974(ColorDistanceDataset):
    whitepoint_xyz100: Any
    c: float
    Y_b: int
    L_A: int
    xyz100_tiles: Any
    is_flat_pair: Any
    def __init__(self) -> None: ...
    def plot(self, cs_class: Type[ColorSpace]): ...
