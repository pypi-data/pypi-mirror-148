from ...cs import ColorSpace
from ..helpers import create_cs_class_instance as create_cs_class_instance, stress_absolute as stress_absolute
from typing import Any, Type

this_dir: Any

class Munsell:
    h: Any
    V: Any
    C: Any
    xyz100: Any
    whitepoint_xyz100: Any
    L_A: int
    c: float
    Y_b: int
    lightness: Any
    def __init__(self) -> None: ...
    def plot(self, cs_class: Type[ColorSpace], V: int): ...
    def plot_lightness(self, cs_class: Type[ColorSpace]): ...
    def stress_lightness(self, cs_class: Type[ColorSpace]) -> float: ...
    stress: Any
