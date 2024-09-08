from abc import ABCMeta, abstractmethod

from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface

from pyganimation._constants import *
import types

class IAnimationBaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self,
                 animation_name: str,
                 animation_script: IAnimationScriptInterface,
                 animation_manager,
                 speed: int | float = 0,
                 loop: bool = False,
                 is_visible: bool = True,
                 is_reversed: bool = False,
                 is_instant_added_to_animation_queue: bool = False,
                 is_removed_from_animation_queue_after_animation_ends: bool = False,
                 animation_info: dict = {
                     ABS_POS: (0, 0),
                     ABS_ANGLE: 0,
                     ABS_SCALE: (1, 1),
                     ABS_ALPHA: 1
                 }
                ):
        """
        """
        pass

    @abstractmethod
    def play(self, start_frame: int | types.NoneType = None, end_frame: int | types.NoneType = None) -> None:
        """
        """
        pass

    @abstractmethod
    def pause(self) -> None:
        """
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        """
        pass

    @abstractmethod
    def replay(self, start_frame: int | types.NoneType = None, end_frame: int | types.NoneType = None) -> None:
        """
        """
        pass

    @abstractmethod
    def reverse(self):
        """
        """
        pass

    @abstractmethod
    def add(self):
        """
        """
        pass

    @abstractmethod
    def remove(self, preserve_internal_information: bool = False):
        """
        """
        pass

    @abstractmethod
    def show(self):
        """
        """
        pass

    @abstractmethod
    def hide(self):
        """
        """
        pass

    @abstractmethod
    def reset(self):
        """
        """
        pass

    @abstractmethod
    def copy(self):
        """
        """
        pass

    @abstractmethod
    def update(self):
        """
        """
        pass

    @abstractmethod
    def draw(self, target_screen):
        """
        """
        pass

    @abstractmethod
    def update_animation_info(self):
        """
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

class IBaseAnimationInterface(IAnimationBaseInterface, metaclass=ABCMeta):
    @abstractmethod
    def _update_current_image_info(self, debugging: bool = False) -> None:
        """
        """
        pass


class IBaseVectorAnimationInterface(IAnimationBaseInterface, metaclass=ABCMeta):
    pass
    

class IAnimationInterface(IAnimationBaseInterface, metaclass=ABCMeta):
    pass

__all__ = [
    "IAnimationBaseInterface",
    "IAnimationInterface",
    "IBaseAnimationInterface",
    "IBaseVectorAnimationInterface"
]
    
