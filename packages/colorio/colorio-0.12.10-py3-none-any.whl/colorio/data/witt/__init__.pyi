from ..color_distance import ColorDistanceDataset as ColorDistanceDataset
from typing import Any

class Witt(ColorDistanceDataset):
    whitepoint_xyz100: Any
    c: float
    L_A: float
    Y_b: float
    def __init__(self) -> None: ...
