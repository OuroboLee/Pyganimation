# AnimationManager class.
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

from pyganimation.core.interface.animation_manager_interface import IAnimationManagerInterface
from pyganimation.core.interface.animation_interface import IBaseAnimationInterface

import pygame

class AnimationManager(IAnimationManagerInterface):
    def __init__(self,
                 target_screen: pygame.Surface,
                 fps: int,
                 debugging: bool = False,
                 play_added_animation_immediatedly: bool = False,
                 remove_ended_animation_immediately: bool = False
                ):
        """
        """
        self._target_screen = target_screen
        self._fps = fps

        self._animation_list = list()

        self._current_master_frame_number = 0

        self._play_added_animation_immediatedly = play_added_animation_immediatedly
        self._remove_ended_animation_immediately = remove_ended_animation_immediately

        self._debugging = debugging

    def all_play(self, start_end_mapping: dict = None) -> None:
        """
        """
        for animation in self._animation_list:
            animation.play()

    def all_pause(self) -> None:
        """
        """
        for animation in self._animation_list:
            animation.pause()

    def all_replay(self, start_end_mapping: dict = None) -> None:
        """
        """
        for animation in self._animation_list:
            animation.replay()

    def all_stop(self) -> None:
        """
        """
        for animation in self._animation_list:
            animation.stop()

    def reset(self) -> list:
        """
        """
        result_animation_list = self._animation_list.copy()
        self._animation_list = []

        return result_animation_list

    def all_show(self) -> None:
        for animation in self._animation_list:
            animation.show()

    def all_hide(self) -> None:
        for animation in self._animation_list:
            animation.hide()

    def all_reverse(self) -> None:
        for animation in self._animation_list:
            animation.reverse()

    def update(self) -> None:
        self._current_master_frame_number += 1
        
        if self._debugging:
            print(f"========== Current Master Frame Number : {self._current_master_frame_number} ==========")

        for animation in self._animation_list:
            animation.update(self._debugging)

    def draw(self) -> None:
        for animation in self._animation_list:
            animation.draw(self._target_screen)

    def add_animation(self, animation: IBaseAnimationInterface):
        self._animation_list.append(animation)
        if self._play_added_animation_immediatedly:
            animation.play()

    def remove_animation(self, animation: IBaseAnimationInterface):
        self._animation_list.remove(animation)

    def process_event(self, event: pygame.Event) -> None:
        pass

    def all_loop(self, loop: int) -> None:
        for animation in self._animation_list:
            animation.loop = loop

    def all_speed(self, speed: float) -> None:
        for animation in self._animation_list:
            animation.speed = speed

    ##### Getter & Setter #####

