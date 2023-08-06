from ..color_distance import ColorDistanceDataset as ColorDistanceDataset
from typing import Any

class Leeds(ColorDistanceDataset):
    whitepoint_xyz100: Any
    c: float
    L_A: int
    Y_b: int
    def __init__(self) -> None: ...
