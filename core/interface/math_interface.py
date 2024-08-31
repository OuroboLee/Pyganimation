from abc import ABCMeta, abstractmethod

from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface

from pyganimation._constants import *

class IBezierCurveInterface(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self,
                 points: list | tuple):
        

        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def _get_final_pos(self, t: float, points: list[tuple]) -> list[tuple] | tuple[float, float]:
        pass

    @abstractmethod
    def get_pos(self, step: float) -> tuple[float, float]:
        pass

    @abstractmethod
    def get_angle(self, step: float) -> float:
        pass

class ICircleInterface(metaclass=ABCMeta):
    pass

class IEillpseInterface(metaclass=ABCMeta):
    pass

class IParabolaInterface(metaclass=ABCMeta):
    pass

class IHyperbolaInterface(metaclass=ABCMeta):
    pass