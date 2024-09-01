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

from pyganimation.core.animation_base import AnimationBase
from pyganimation.core.interface.animation_interface import IAnimationInterface
from pyganimation.core.interface.animation_script_interface import IAnimationTimelineInterface, IAnimationListInterface
from animation_manager import AnimationManager
from pyganimation._constants import *

import types
import pygame

class Animation(AnimationBase, IAnimationInterface):
    def __init__(self, 
                 animation_name: str, 
                 animation_manager: AnimationManager,
                 animation_timeline: IAnimationTimelineInterface,
                 animation_list: IAnimationListInterface,
                 speed: int = 1,
                 loop: bool = False,
                 is_visible: bool = True,
                 is_reversed: bool = False,
                 is_instant_added_to_animation_queue: bool = False,
                 is_instant_removed_from_animation_queue_after_animation_ends: bool = False,
                 animation_info: dict = {
                     ABS_POS: (0, 0),
                     ABS_ANGLE: 0,
                     ABS_SCALE: (1, 1),
                     ABS_ALPHA: 1
                 }
                ):
        
        super().__init__(
            animation_name, 
            animation_manager,
            animation_info,
            speed,
            loop,
            is_visible,
            is_reversed,
            is_instant_added_to_animation_queue,
            is_instant_removed_from_animation_queue_after_animation_ends
        )

        self._animation_timeline = animation_timeline
        self._animation_list = animation_list

        self._total_frame = self._animation_timeline.get_total_frame()

        self._animation_current_frame_number = 1
        self._animation_current_internal_frame_number = 1
        self._animation_start_frame_number = 1
        self._animation_end_frame_number = self._total_frame - 1

    def copy(self):
        return Animation(
            self._animation_name,
            self._animation_manager,
            self._animation_timeline,
            self._animation_list,
            self._speed,
            self._loop,
            self.is_visible,
            self._is_reversed,
            self._is_instant_added_to_animation_queue,
            self._is_instant_removed_from_animation_queue_after_animation_ends
        )

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


    