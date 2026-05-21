from dataclasses import dataclass


@dataclass(slots=True)
class BBox:
    x0: float
    y0: float
    x1: float
    y1: float
