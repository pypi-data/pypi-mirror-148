import numpy as np
from ..cs import ColorCoordinates as ColorCoordinates, ColorSpace as ColorSpace, convert as convert
from .helpers import create_cs_class_instance as create_cs_class_instance
from numpy.typing import ArrayLike as ArrayLike
from typing import Any, Type

class HueLinearityDataset:
    name: Any
    whitepoint_xyz100: Any
    arms: Any
    neutral_gray: Any
    def __init__(self, name: str, whitepoint_xyz100: ArrayLike, arms, neutral_gray: Union[ArrayLike, None] = ...) -> None: ...
    def plot(self, cs_class: Type[ColorSpace]): ...
    def stress(self, cs_class: Type[ColorSpace]) -> np.ndarray: ...
