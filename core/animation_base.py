# Base class of BaseAnimation / BaseVectorAnimation / Animation class.
# Only for internal use.
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
#
# TODO: 
#


from pyganimation.core.interface import IAnimationManagerInterface, IAnimationBaseInterface, IAnimationInterface
from pyganimation import INF

import types
from typing import Any
import pygame

class AnimationBase(IAnimationBaseInterface):
    def __init__(self,
                 animation_name: str,
                 animation_manager: IAnimationManagerInterface,
                 animation_info: dict,
                 speed: int | float = 1,
                 loop: int = 1,
                 is_visible: bool = True,
                 is_reversed: bool = False,
                 is_instant_added_to_animation_queue: bool = False,
                 is_instant_removed_from_animation_queue_after_animation_ends: bool = False
                 ):
        """
        Initializes AnimationBase instance.

        :param animation_name: The name of animation.
        :param animation_manager: The manager that handles this animation.
        :param animation_info: The information of animation. The writing rule is work in process.
        :param speed: The speed of animation.
        :param loop: If this animation loops or not. If negative int, the animation repeats forever. If positive int, the animation repeats as much as the number. If 0, the animation won't be played.
        :param is_visible: If this animation is visible or not.
        :param is_reversed: If this animation is reversed or not.
        :param is_instant_added_to_animation_queue: If this animation is added to animation queue instantly after declaration.
        :param is_instant_removed_from_animation_queue_after_animation_ends: If this animation removed instantly after the animation ended. 
        """

        self._animation_name = animation_name
        self._animation_manager = animation_manager
        self._animation_info = animation_info

        self._speed = speed
        self._loop = loop if loop >= 0 else INF
        self._start_loop = self._loop

        self._is_visible = is_visible
        self._is_reversed = is_reversed
        self._is_instant_added_to_animation_queue = is_instant_added_to_animation_queue
        self._is_instant_removed_from_animation_queue_after_animation_ends = is_instant_removed_from_animation_queue_after_animation_ends

        self._animation_current_internal_frame_number = 1
        self._animation_current_frame_number = 1
        self._animation_start_frame_number = 1

        self._is_playing = False

        self._parent = None
        self._animation_abs_start_frame_number = None
        self._children = None

        self._added_to_animation_queue = False

        if self._is_instant_added_to_animation_queue:
            self.add()

        # Need to be reset in child class's initializing process.
        self._total_frame = None
        self._animation_end_frame_number = None
        self._substantial_total_frame = None

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def play(self, start_frame: int | types.NoneType = None, end_frame: int | types.NoneType = None) -> None:
        """
        Plays animation from start_frame to end_frame.

        :param start_frame: The frame number that animation starts from.
        :param end_frame: The frame number that animation ends at.
                          If None, animation will end at final frame stated at animation script.
        """
        self.start_frame = start_frame
        self.end_frame = end_frame

        self._is_playing = True

        if start_frame is not None:
            self._animation_start_frame_number = start_frame
        else:
            self._animation_start_frame_number = 1

        if end_frame is not None:
            self._animation_end_frame_number = end_frame
        else: 
            self._animation_end_frame_number = self._total_frame - 1

    def pause(self) -> None:
        """
        Pauses animation.
        """
        self._is_playing = False

    def stop(self) -> None:
        """
        Stops animation.
        """
        self._is_playing = False
        self._loop = self._start_loop

        self._reset_frame_number(self._is_reversed)

    def reset(self, stops_animation: bool = False) -> None:
        """
        Resets all inner data of the animation, which had been gotten by non-necessary parameter.

        :param stops_animation: If stops the animation or not.
        """
        self._animation_start_frame_number = 1
        self._animation_end_frame_number = self._total_frame - 1

        self._loop = 1
        self._start_loop = 1

        self._speed = 1
        self._is_visible = True
        self._is_reversed = False

        if stops_animation: pass
        # .
        # .
        # .
        # Additional operations need to be written in child classes.
        #
            
    def _reset_frame_number(self, reverse: bool):
        if not reverse:
            self._animation_current_frame_number = self._animation_start_frame_number
            self._animation_current_internal_frame_number = self._animation_start_frame_number
        else:
            self._animation_current_frame_number = self._animation_end_frame_number
            self._animation_current_internal_frame_number = self._animation_end_frame_number

    def replay(self, start_frame: int | types.NoneType = None, end_frame: int | types.NoneType = None) -> None:
        """
        Replays animation from start_frame to end_frame.

        :param start_frame: The frame number that animation starts from.
        :param end_frame: The frame number that animation ends at. \n
                          If None, animation will end at final frame stated at animation script.
        """
        self.stop()
        self.play(start_frame, end_frame)

    def reverse(self) -> None:
        """
        Reverses animation's playback direction.
        """
        self._is_reversed = not self._is_reversed

    def add(self) -> None:
        """
        Adds this animation in animation manager's animation queue.
        """
        if not self._added_to_animation_queue:
            self._added_to_animation_queue = True
            self._animation_manager.add_animation(self)
        else:
            pass

    def remove(self, preserve_internal_information: bool = False) -> None:
        """
        Removes this animation from animation manager's animation queue.

        :param preserve_internal_information: 
        """
        if self._added_to_animation_queue:
            self._added_to_animation_queue = False
            self._animation_manager.remove_animation(self)

        if not preserve_internal_information:
            self.stop()

    def show(self) -> None:
        """
        Shows animation.
        """
        self._is_visible = True
    
    def hide(self) -> None:
        """
        Hides animation.
        """
        self._is_visible = False

    def update_animation_info(self, flag: str, value: tuple[float, float] | float) -> None:
        """
        Updates animation info.
        """
        self._animation_info[flag] = value

    def copy(self) -> Any:
        """
        Copies animation.

        Need to be overrided by chlid class.
        """
        pass

    def update(self, debugging: bool = False):
        """
        Update animation's current frame number and current image info.
        Need to be overrided by chlid class.

        :param debugging: If prints debugging information of this animation update process or not.
        """
        pass

    def draw(self, target_screen: pygame.Surface):
        """
        Draws animation on target_screen.
        Need to be overrided by chlid class.

        :param target_screen: The screen surface which this animation is drawn on.
        """
        pass

    ##### Getter & Setter #####

    def _get_speed(self) -> int:
        return self._speed
    
    def _set_speed(self, speed: int | float) -> None:
        if type(speed) not in (int, float): 
            raise ValueError("Speed must be int | float larger than 0.")
        if speed <= 0:
            raise ValueError("Speed must be int | float larger than 0.")
        self._speed = speed

    speed = property(_get_speed, _set_speed)

    def _get_name(self) -> str:
        return self._animation_name
    
    def _set_name(self, name: str) -> None:
        if type(name) != str: 
            raise ValueError("Name must be str.")
        self._name = name

    animation_name = property(_get_name, _set_name)

    def _get_loop(self) -> int:
        return self._loop if self._loop is not INF else -1
    
    def _set_loop(self, loop: int) -> None:
        if type(loop) != int: 
            raise ValueError("Loop must be int.")
        self._loop = loop if loop >= 0 else INF

    loop = property(_get_loop, _set_loop)

    def _get_is_visible(self) -> bool:
        return self._is_visible
    
    def _set_is_visible(self, value: bool) -> None:
        if type(value) != bool: 
            raise ValueError("Is_visible must be bool.")
        self._is_visible = value

    is_visible = property(_get_is_visible, _set_is_visible)

    def _get_is_reversed(self) -> bool:
        return self._is_reversed
    
    def _set_is_reversed(self, value: bool) -> None:
        if type(value) != bool:
            raise ValueError("Is_reversed must be bool.")
        self._is_reversed = value

    is_reversed = property(_get_is_reversed, _set_is_reversed)

    def _get_is_playing(self) -> bool:
        return self._is_playing
    
    def _set_is_playing(self, value: bool) -> None:
        if type(value) != bool:
            raise ValueError("Is_playing must be bool.")
        self._is_playing = value

    is_playing = property(_get_is_playing, _set_is_playing)

    def _get_start_frame(self) -> int:
        return self._animation_start_frame_number
    
    def _set_start_frame(self, number: int | types.NoneType) -> None:
        if type(number) == int:
            if number <= 0 or number >= self._total_frame - 1:
                raise ValueError("Start frame must be integer type between 1 and self.total_frame - 1, or None.")

            if number == self._animation_end_frame_number:
                raise ValueError("Start frame must be different from end frame.")

            self._animation_start_frame_number = number
        
        elif type(number) == types.NoneType:
            self._animation_start_frame_number = 1

        else:
            raise ValueError("Start frame must be integer type between 1 and self.total_frame - 1, or None.")
        
    start_frame = property(_get_start_frame, _set_start_frame)

    def _get_end_frame(self) -> int:
        return self._animation_end_frame_number
    
    def _set_end_frame(self, number: int | types.NoneType) -> None:
        if type(number) == int:
            if number <= 0 or number >= self._total_frame - 1:
                raise ValueError("End frame must be integer between 1 and self.total_frame - 1, or None.")

            if number == self._animation_end_frame_number:
                raise ValueError("End frame must be different from start frame.")

            self._animation_end_frame_number = number
        
        elif type(number) == types.NoneType:
            self._animation_end_frame_number = self._total_frame - 1

        else:
            raise ValueError("End frame must be integer between 1 and self.total_frame - 1, or None.")
        
    end_frame = property(_get_end_frame, _set_end_frame)

    def _get_abs_start_frame(self) -> int:
        return self._animation_abs_start_frame_number
    
    def _set_abs_start_frame(self, number: int) -> None:
        if type(number) != int:
            raise ValueError("Abs start frame must be integer equal or larger than 0.")

        else:
            if number < 0:
                raise ValueError("Abs start frame must be integer equal or larger than 0.")
        
        self._animation_abs_start_frame_number = number
    
    abs_start_frame = property(_get_abs_start_frame, _set_abs_start_frame)

    def _get_added_to_animation_queue(self) -> bool:
        return self._added_to_animation_queue
    
    def _set_added_to_animation_queue(self, value: bool) -> None:
        if type(value) != bool:
            raise ValueError("The value must be boolean.")
        
        self._added_to_animation_queue = value

    added_to_animation_queue = property(_get_added_to_animation_queue, _set_added_to_animation_queue)

    def _get_parent(self) -> IAnimationInterface | None:
        return self._parent
    
    def _set_parent(self, parent: IAnimationInterface | types.NoneType) -> None:
        if type(parent) not in (IAnimationInterface, types.NoneType):
            raise ValueError("Parent must be Animation object or None.")
        self._parent = parent

    parent = property(_get_parent, _set_parent)

    def _get_children(self) -> list[IAnimationBaseInterface] | None:
        return self._children
    
    def _set_children(self, children: list[IAnimationBaseInterface] | types.NoneType) -> None:
        if type(children) not in (list, types.NoneType):
            raise ValueError("Children must be list containing at least one Animation | BaseAnimation | BaseVectorAnimation Object, or None.")
        else:
            if type(children) == list:
                for idx, child in enumerate(children):
                    if type(child) != IAnimationBaseInterface:
                        raise ValueError(f"Children must be list containing at least one Animation | BaseAnimation | BaseVectorAnimation Object, or None. => Invalid object in idx {idx}.")

        self._children = children

    children = property(_get_children, _set_children)

    def _get_animation_info(self) -> dict:
        return self._animation_info
    
    def _set_aniamtion_info(self, info: dict):

        self._animation_info = info

    animation_info = property(_get_animation_info, _set_aniamtion_info)

    def _get_current_frame(self):
        return self._animation_current_frame_number
    
    def _set_current_frame(self, number: int):
        if type(number) != int:
            raise ValueError("Number must be integer between 0 and total_frame.")
        else:
            if number <= 0 or number < self._total_frame:
                raise ValueError("Number must be interger between 0 and total_frame.")
            
        self._animation_current_frame_number = number
        self._animation_current_internal_frame_number = number
        
    current_frame = property(_get_current_frame, _set_current_frame)
    
    def _get_manager(self):
        return self._animation_manager
    
    def _set_manager(self, manager):
        if type(manager) != IAnimationManagerInterface:
            raise ValueError("manager must be AnimatonManager Instance.")
        
        self._animation_manager = manager

    animation_manager = property(_get_manager, _set_manager)
        
    def get_total_frame(self) -> int:
        return self._total_frame
    
    def get_substantial_total_frame(self) -> float:
        return self._substantial_total_frame

    