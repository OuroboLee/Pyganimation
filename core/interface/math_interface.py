from abc import ABCMeta, abstractmethod

from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface

from pyganimation._constants import *
import pygame

class IAnchorInterface(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self, scale_anchor, angle_anchor, rect: pygame.Rect, scale: tuple, angle: int | float):
        pass

    @abstractmethod
    def modify_pos(self, pos: tuple) -> tuple:
        pass

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
    @abstractmethod
    def __init__(self, center: list[float, float] | tuple[float, float]):
        pass
    
    @abstractmethod
    def _get_angle_from_pos(self, pos: list | tuple) -> float:
        pass

    @abstractmethod
    def _get_pos_from_angle(self, angle: float) -> tuple[float, float]:
        pass

    @abstractmethod
    def get_pos(self, start_angle: float, total_angle: float, step: float) -> tuple[float, float]:
        pass

    @abstractmethod
    def get_angle(self, start_angle: float, total_angle: float, step: float) -> float:
        pass

class IEillpseInterface(metaclass=ABCMeta):
    pass

class IParabolaInterface(metaclass=ABCMeta):
    pass

class IHyperbolaInterface(metaclass=ABCMeta):
    pass