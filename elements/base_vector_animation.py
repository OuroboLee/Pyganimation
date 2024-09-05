# BaseVectorAnimation class.
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


import pygame

from pyganimation.core.interface.animation_interface import IBaseVectorAnimationInterface, IAnimationInterface
from pyganimation.core.interface.animation_manager_interface import IAnimationManagerInterface
from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface

from pyganimation._constants import *
from pyganimation.core.animation_base import AnimationBase
from pyganimation.core.math.interpolate_functions import scale_anchor_interpret, angle_anchor_interpret
from pyganimation.core.math.tools import is_positive

from typing import Any
import types

class BaseVectorAnimation(AnimationBase, IBaseVectorAnimationInterface):
    def __init__(self,
                 animation_name: str,
                 animation_script: IAnimationScriptInterface,
                 animation_manager: IAnimationManagerInterface,
                 speed: int | float = 1,
                 loop: int = 1,
                 is_visible: bool = True,
                 is_reversed: bool = False,
                 is_instant_added_to_animation_queue: bool = False,
                 is_instant_removed_from_animation_queue_after_animation_ends: bool = False,
                 animation_info: dict = NORMAL_ANIMATION_INFO_DEFAULT.copy()
                 ):
        """
        Initializes BaseAnimation instance.

        :param animation_name: The name of animation.
        :param animation_script: The script of animation.
        :param animation_manager: The manager that handles this animation.
        :param speed: The speed of animation.
        :param loop: If this animation loops or not. If negative int, the animation repeats forever. If positive int, the animation repeats as much as the number. If 0, the animation won't be played.
        :param is_visible: If this animation is visible or not.
        :param is_reversed: If this animation is reversed or not.
        :param is_instant_added_to_animation_queue: If this animation is added to animation queue instantly after declaration.
        :param is_instant_removed_from_animation_queue_after_animation_ends: If this animation removed instantly after the animation ended. 
        :param animation_info: The information of animation. The writing rule is work in process.
        """
        
        if animation_script.get_script_type() not in (SCRIPTTYPE_NORMAL_VECTOR_ANIMATION, SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION):
            raise ValueError("Invaild animation script.")

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

        self._animation_script = animation_script

        self._current_shape = self._animation_script[0][SHAPE_INFO][TARGET]
        self._current_shape_info = None


        self._total_frame = animation_script.get_total_frame()
        self._animation_end_frame_number = self._total_frame - 1
        self._substantial_total_frame = self._total_frame * (1 / self._speed) * self._loop if self._loop is not INF else INF

    def __str__(self) -> str:
        return ""
    
    def __repr__(self) -> str:
        return ""

    def stop(self) -> None:
        """
        Stops animation.
        """
        super().stop()

        self._current_shape = self._animation_script[0][SHAPE_INFO][TARGET]
        self._current_shape_info = None

    def reset(self, stops_animation: bool = False) -> None:
        """
        Resets all inner data of the animation, which had been gotten by non-necessary parameter.

        :param stops_animation: If stops the animation or not.
        """
        super().reset()

        if stops_animation: self.stop()

    def copy(self) -> IBaseVectorAnimationInterface:
        pass

    def update(self, debugging: bool = False) -> None:
        """
        Update animation's current frame number and current image info.

        :param debugging: If prints debugging information of this animation update process or not.
        """

        if self._is_playing:
            if self._loop != 0:
                if not self._is_reversed:
                    self._animation_current_internal_frame_number += 1 * self._speed
                    self._animation_current_frame_number = round(self._animation_current_internal_frame_number)
                    if self._animation_current_frame_number <= self._animation_end_frame_number:
                        self._update_current_shape_info(debugging)
                    else:
                        if self._loop is INF or self._loop > 0: 
                            self._reset_frame_number(self._is_reversed)

                            if self._loop is not INF: self._loop -= 1
                            
                else:
                    self._animation_current_internal_frame_number -= 1 * self._speed
                    self._animation_current_frame_number = round(self._animation_current_internal_frame_number)
                    if self._animation_current_frame_number >= self._animation_start_frame_number:
                        self._update_current_shape_info(debugging)
                            
                    else:
                        if self._loop is INF or self._loop > 0: 
                            self._reset_frame_number(self._is_reversed)

                            if self._loop is not INF: self._loop -= 1
            else:
                self._is_playing = False
                if self._is_instant_removed_from_animation_queue_after_animation_ends:
                    self.remove()

        if debugging:
            self._update_debugging()

    def _update_debugging():
        pass

    def _update_current_shape_info(self, debugging: bool = False) -> types.NoneType:
        current_frame_info = self._animation_script[self._animation_current_frame_number]

        current_frame_shape_info = current_frame_info[SHAPE_INFO]

        self._current_shape = current_frame_shape_info[TARGET]
        self._current_shape_info = current_frame_shape_info[INFO]

    def copy(self):
        """
        Copies animation.
        """
        return BaseVectorAnimation(
            self._animation_name,
            self._animation_script,
            self._animation_manager,
            self._speed,
            self._start_loop,
            self._is_visible,
            self._is_reversed,
            self._is_instant_added_to_animation_queue,
            self._is_instant_removed_from_animation_queue_after_animation_ends,
            self._animation_info
        )

    def draw(self, target_screen: pygame.Surface) -> None:
        """
        """
        if self._animation_current_frame_number <= self._total_frame:
            # print(self.animation_script[self.animation_current_frame_number])
            current_relative_pos = self._animation_script[self._animation_current_frame_number][POS]
            current_relative_angle = self._animation_script[self._animation_current_frame_number][ANGLE]
            current_relative_scale = self._animation_script[self._animation_current_frame_number][SCALE]
            current_relative_alpha = self._animation_script[self._animation_current_frame_number][ALPHA]
            current_relative_color = self._animation_script[self._animation_current_frame_number][COLOR]

            current_pos = (current_relative_pos[0] + self.animation_info[ABS_POS][0], current_relative_pos[1] + self.animation_info[ABS_POS][1])
            current_angle = current_relative_angle + self.animation_info[ABS_ANGLE]
            current_scale = (current_relative_scale[0] * self.animation_info[ABS_SCALE][0], current_relative_scale[1] * self.animation_info[ABS_SCALE][1])
            current_flip = (False if is_positive(current_scale[0]) else True, False if is_positive(current_scale[1]) else True)
            current_alpha = int(current_relative_alpha * self.animation_info[ABS_ALPHA]) if self.is_visible else 0

            current_color = [
                int(current_relative_color[0] * self.animation_info[ABS_COLOR][0]),
                int(current_relative_color[1] * self.animation_info[ABS_COLOR][1]),
                int(current_relative_color[2] * self.animation_info[ABS_COLOR][2]),
            ]

            # Correction in alpha & color

            if current_alpha > 255: current_alpha = 255
            elif current_alpha < 0: current_alpha = 0

            if current_color[0] > 255: current_color[0] = 255
            elif current_color[0] < 0: current_color[0] = 0
            if current_color[1] > 255: current_color[1] = 255
            elif current_color[1] < 0: current_color[1] = 0
            if current_color[2] > 255: current_color[2] = 255
            elif current_color[2] < 0: current_color[2] = 0

            

            
            
            if self._current_shape == ELLIPSE:
                pass

            elif self._current_shape == RECTANGLE:
                target_rect = self._animation_script[0][SHAPE_INFO][INFO]
                target_colorkey = self._animation_info[COLORKEY]
                target_surface = pygame.Surface((target_rect.width * current_scale[0], target_rect.height * current_scale[1]), pygame.SRCALPHA)

                target_surface.set_colorkey(target_colorkey)
                target_surface.set_alpha(current_alpha)

                target_surface.fill(current_color)

                manipulated_image = pygame.transform.rotate(target_surface, current_angle)
                manipulated_image_rect = manipulated_image.get_rect()
                manipulated_image_rect.center = current_pos

                target_screen.blit(target_surface, manipulated_image_rect)
                    

            elif self._current_shape == SQUARE: 
                pass

            elif self._current_shape == CIRCLE:
                pass

    ##### Getter & Setter #####

    def get_animation_script(self) -> IAnimationScriptInterface:
        return self._animation_script

    
        