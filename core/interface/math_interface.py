from abc import ABCMeta, abstractmethod

from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface

from pyganimation._constants import *

class IBezierCurveInterface(metaclass = ABCMeta):
    def __init__(self,
                 points: list | tuple):
        

        pass

    def __str__(self) -> str:
        pass

    