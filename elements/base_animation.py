# BaseAnimation class.
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

from pyganimation.core.interface.animation_interface import IBaseAnimationInterface, IAnimationInterface
from pyganimation.core.interface.animation_manager_interface import IAnimationManagerInterface
from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface

from pyganimation._constants import *
from pyganimation.core.animation_base import AnimationBase
from pyganimation.elements.script_converter import scale_anchor_interpret, angle_anchor_interpret

from typing import Any
import types

class BaseAnimation(AnimationBase, IBaseAnimationInterface):
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
        
        if animation_script.get_script_type() not in (SCRIPTTYPE_NORMAL_NORMAL_ANIMATION, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION):
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

        self._current_image = self._animation_script[0][IMAGE_INFO][TARGET] # pygame.Surface
        self._current_image_rect = None

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

        self._current_image = self._animation_script[0][IMAGE_INFO][TARGET]
        self._current_image_rect = None

    def reset(self, stops_animation: bool = False) -> None:
        """
        Resets all inner data of the animation, which had been gotten optional parameters.

        :param stops_animation: If stops the animation or not.
        """
        super().reset()

        if stops_animation: self.stop()

    def copy(self) -> IBaseAnimationInterface:
        """
        Copies animation.
        """
        return BaseAnimation(
            self._animation_name,
            self._animation_script,
            self._animation_manager,
            self._speed,
            self._loop,
            self._is_visible,
            self._is_reversed,
            self._is_instant_added_to_animation_queue,
            self._animation_info
        )

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
                        self._update_current_image_info()
                    else:
                        if self._loop is INF or self._loop > 0: 
                            self._reset_frame_number(self._is_reversed)

                            if self._loop is not INF: self._loop -= 1
                            
                else:
                    self._animation_current_internal_frame_number -= 1 * self._speed
                    self._animation_current_frame_number = round(self._animation_current_internal_frame_number)
                    if self._animation_current_frame_number >= self._animation_start_frame_number:
                        self._update_current_image_info()
                            
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

    def _update_current_image_info(self) -> None:
        current_frame_info = self._animation_script[self._animation_current_frame_number]

        # print(self._animation_current_frame_number, ":", current_frame_info)

        current_frame_image_info = current_frame_info[IMAGE_INFO]
        current_frame_target = current_frame_image_info[TARGET]

        self._current_image = current_frame_target
        if self._animation_info[COLORKEY] is not None:
            self._current_image.set_colorkey(self._animation_info[COLORKEY])
            
        if current_frame_image_info[RECT] != 0:
            self._current_image_rect = current_frame_image_info[RECT]
        else:
            self._current_image_rect = None

    def _update_debugging(self):
        print(f"-------------------- {self._animation_name}, No.{self._animation_current_frame_number} Frame --------------------")
        print(f"\tFrom {self._animation_start_frame_number} to {self._animation_end_frame_number}")
        print(f"is_playing: {self._is_playing}")
        print(f"is_reversed: {self._is_reversed}")
        print(f"is_visible: {self._is_visible}")
        print(f"loop: {self._loop}")
        print(f"speed: {self._speed}")
        print()
        print(f"Current Internal Frame Number: {self._animation_current_internal_frame_number}")
        print(f"Current Image Info: {self._current_image}, {self._current_image_rect}")
        print(f"Current Frame Info: {self._animation_script[self._animation_current_frame_number]}")
        print()
        

    def draw(self, target_screen: pygame.Surface) -> None:
        """
        Draws animation on target_screen.

        :param target_screen: The screen surface which this animation is drawn on.
        """
        if self._animation_current_frame_number <= self._total_frame and self._is_visible:
            # print(self.animation_script[self._animation_current_frame_number])
            current_relative_pos = self._animation_script[self._animation_current_frame_number][POS]
            current_relative_angle = self._animation_script[self._animation_current_frame_number][ANGLE]
            current_relative_scale = self._animation_script[self._animation_current_frame_number][SCALE]
            current_relative_alpha = self._animation_script[self._animation_current_frame_number][ALPHA]

            current_pos = (current_relative_pos[0] + self._animation_info[ABS_POS][0], current_relative_pos[1] + self._animation_info[ABS_POS][1])
            current_angle = current_relative_angle + self._animation_info[ABS_ANGLE]
            current_scale = (current_relative_scale[0] * self._animation_info[ABS_SCALE][0], current_relative_scale[1] * self._animation_info[ABS_SCALE][1])
            current_alpha = int(current_relative_alpha * self._animation_info[ABS_ALPHA])

            # ANCHORING
            current_scale_anchor = self._animation_script[self._animation_current_frame_number][SCALE_ANCHOR]
            current_pos = scale_anchor_interpret(
                current_scale_anchor, self._current_image.get_rect(),
                current_pos, current_scale
            )
            print(f"POS: {current_pos}")

            current_angle_anchor = self._animation_script[self._animation_current_frame_number][ANGLE_ANCHOR]
            current_pos = angle_anchor_interpret(
                current_angle_anchor, self._current_image.get_rect(),
                current_pos, current_scale, current_angle
            )

            if current_alpha > 255: 
                current_alpha = 255
            elif current_alpha < 0: 
                current_alpha = 0
            
            self._current_image.set_alpha(current_alpha)

            manipulated_image = pygame.transform.scale_by(self._current_image, current_scale)
            manipulated_image = pygame.transform.rotate(manipulated_image, current_angle)
            manipulated_image_rect = manipulated_image.get_rect()
            manipulated_image_rect.center = current_pos
                
            if self._current_image_rect is not None:
                target_screen.blit(
                    manipulated_image, manipulated_image_rect, 
                    (self._current_image_rect.x, self._current_image_rect.y, self._current_image_rect.width, self._current_image_rect.height)
                    )
            else:
                target_screen.blit(manipulated_image, manipulated_image_rect)
                # print(f"{self._animation_current_frame_number} : {manipulated_image_rect}")

    ##### Getter & Setter #####
    
if __name__ == "__main__":
    from pyganimation.elements.animation_script import AnimationScript
    from pyganimation.elements.script_converter import keyframe_normal_to_normal_normal

    keyframe_script = {
        0: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((50, 50)),
                RECT: None
            },
            KEYFRAME_NORMAL_INFO: {
                POS: (0, 0),
                SCALE: (1, 1)
            }
        },
        20: {
            KEYFRAME_NORMAL_INFO: {
                SCALE: (0.7, 1.3)
            },
            KEYFRAME_INTERPOLATE_INFO: {
                SCALE: SIN_IN,
                SCALE_ANCHOR: TOPMID
            }
        },
        40: {
            KEYFRAME_NORMAL_INFO: {
                SCALE: (1, 1)
            },
            KEYFRAME_INTERPOLATE_INFO: {
                SCALE: SIN_IN,
                SCALE_ANCHOR: TOPMID
            }
        }
    }
    normal_script = keyframe_normal_to_normal_normal(keyframe_script)
    script = AnimationScript(normal_script)