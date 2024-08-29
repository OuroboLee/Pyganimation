# Animation class.
#
# Adding Instructions...
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# TODO: 
#


from core.interface.animation_interface import IAnimationInterface, IBaseAnimationInterface, IBaseVectorAnimationInterface
from core.interface.animation_script_interface import IAnimationTimelineInterface
from animation_manager import AnimationManager
from pyganimation._constants import *

import types
import pygame

class Animation(IAnimationInterface):
    def __init__(self, 
                 animation_name: str, 
                 animation_manager: AnimationManager,
                 animation_timeline: IAnimationTimelineInterface,
                 animation_list: list,
                 speed: int = 1,
                 loop: bool = False,
                 is_visible: bool = True,
                 is_reversed: bool = False,
                 is_instant_added_to_animaiton_queue: bool = False,
                 is_instant_removed_from_animation_queue_after_animation_ends: bool = False,
                 animation_info: dict = {
                     ABS_POS: (0, 0),
                     ABS_ANGLE: 0,
                     ABS_SCALE: (1, 1),
                     ABS_ALPHA: 1
                 }
                ):
        assert len(animation_list) > 0, "Must contain at least one BaseAnimation / BaseVectorAnimation / Animation object."
        for a in animation_list:
            assert type(a) == str, "Invaild argument. Arguments must contain at least one BaseAnimation / BaseVectorAnimation / Animation object."

        self._animation_name = animation_name
        self._animation_manager = animation_manager
        self._animation_timeline = animation_timeline
        self._animation_list = animation_list

        self._speed = speed
        self._loop = loop
        self._is_visible = is_visible
        self._is_reversed = is_reversed
        self._is_instant_added_to_animation_queue = is_instant_added_to_animaiton_queue
        self._animation_info = animation_info

        self._total_frame = self._animation_timeline.get_total_frame()

        self._parent = None
        self._children = None
    
    def play(self, start_frame: int | types.NoneType = None, end_frame: int | types.NoneType = None) -> None:
        pass

    def pause(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def replay(self, start_frame: int | types.NoneType = None, end_frame: int | types.NoneType = None) -> None:
        pass

    def reverse(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass

    def show(self):
        pass

    def hide(self):
        pass

    def copy(self):
        pass

    def update(self):
        pass

    def draw(self, target_screen: pygame.Surface):
        pass

    def update_animation_info(self, flag, value):
        self._animation_info[flag] = value

    def __str__(self):
        pass

    def __repr__(self):
        pass


    