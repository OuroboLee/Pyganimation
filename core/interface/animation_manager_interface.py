from abc import ABCMeta, abstractmethod

from pyganimation.core.interface.animation_interface import IBaseAnimationInterface
import pygame
from typing import Any

class IAnimationManagerInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def all_pause(self):
        """
        Pause all playing animations.
        """
        pass

    @abstractmethod
    def all_play(self):
        """
        Play all paused animations.
        """
        pass

    @abstractmethod
    def all_stop(self):
        """
        """
        pass

    @abstractmethod
    def all_replay(self):
        """
        Replay all animations.
        """
        pass

    @abstractmethod
    def all_reverse(self):
        """
        Reverse all animations.
        """
        pass

    @abstractmethod
    def all_show(self):
        """
        Makes all animations invisible. Animation that has been invisible still can be played.
        """
        pass

    @abstractmethod
    def all_hide(self):
        """
        Makes all animations visible.
        """
        pass

    @abstractmethod
    def all_loop(self, value: int):
        pass

    @abstractmethod
    def all_reverse(self, bool: bool):
        pass

    @abstractmethod
    def reset(self):
        """
        """
        pass

    @abstractmethod
    def update(self):
        """
        """
        pass

    @abstractmethod
    def draw(self):
        """
        """
        pass

    @abstractmethod
    def add_animation(self, animation_object: IBaseAnimationInterface):
        """
        """
        pass

    @abstractmethod
    def remove_animation(self, animation_object: IBaseAnimationInterface):
        """
        """
        pass

    @abstractmethod
    def process_event(self, event: pygame.Event) -> None:
        pass

    ##### Getter & Setter #####

__all__ = [
    "IAnimationManagerInterface"
]