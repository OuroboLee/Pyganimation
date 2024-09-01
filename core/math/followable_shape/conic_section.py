from pyganimation.core.math.followable_shape import FollowableShape

from math import sin, cos, tan, pi, radians, degrees, asin, acos, atan

def polar_to_orth(r: float, theta: float) -> tuple[float, float]:
    """
    Converts polar coordinate to orthology coordinate.

    :param r: Radius.
    :param c: Degree in radian.
    """
    return r * cos(theta), r * sin(theta)

def orth_to_polar(x: float, y: float) -> tuple[float, float]:
    """
    Converts orthology coordinate to polar coordinate.

    :param x: X Coordinate.
    :param y: Y Coordinate.
    """
    return (x ** 2 + y ** 2) ** 0.5, atan(y / x)

class Circle(FollowableShape):
    pass

class Eillpse(FollowableShape):
    pass

class Parabola(FollowableShape):
    pass

class Hyperbola(FollowableShape):
    pass

__all__ = [
    "Circle",
    "Eillpse",
    "Parabola",
    "Hyperbola"
]

