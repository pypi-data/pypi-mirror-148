from ..cs import ColorCoordinates as ColorCoordinates, ColorSpace as ColorSpace, convert as convert, string_to_cs as string_to_cs
from typing import Any

class EllipseDataset:
    name: Any
    centers: Any
    points: Any
    def __init__(self, name: str, centers: ColorCoordinates, points: ColorCoordinates) -> None: ...
    def stress(self, cs: ColorSpace): ...
    def plot(self, cs: Union[ColorSpace, str], ellipse_scaling: float = ...): ...
