from numpy.typing import ArrayLike as ArrayLike
from typing import Any

class SpectralData:
    name: Any
    lmbda_nm: Any
    data: Any
    def __init__(self, lmbda_nm: ArrayLike, data: ArrayLike, name: Union[str, None] = ...) -> None: ...
