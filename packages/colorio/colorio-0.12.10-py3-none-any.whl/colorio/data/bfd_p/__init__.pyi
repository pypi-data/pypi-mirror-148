from ...cs import ColorSpace
from ..helpers import create_cs_class_instance as create_cs_class_instance, stress_absolute as stress_absolute, stress_relative as stress_relative
from typing import Any, Callable, Type

class BfdP:
    c: float
    L_A: int
    Y_b: int
    target_dist: Any
    xyz_pairs: Any
    whitepoints: Any
    def __init__(self) -> None: ...
    def stress(self, cs_class: Type[ColorSpace], variant: str = ...): ...
    def stress_lab_diff(self, fun: Callable, variant: str = ...) -> float: ...
