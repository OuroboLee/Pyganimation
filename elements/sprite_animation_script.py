from pyganimation.core.validation_check import *
from pyganimation.core.interface.animation_script_interface import ISpriteAnimationScriptInterface
from pyganimation.core.animation_file_manager import load
from pyganimation.core.converter.script_converter import keyframe_normal_to_normal_normal
from pyganimation._constants import *

import pygame
import pprint, types, os

class SpriteAnimationScript(ISpriteAnimationScriptInterface):
    def __init__(self,
                 script: list | str,
                 debugging: bool = False
                 ):
        if type(script) not in (list, str):
            raise TypeError("Script parameter must be among path-like str that represents json format file or Python list.")

        self._debugging = debugging

        self._script_path = None
        self._primitive_script = None

        self._total_frame = 0

        self._final_script = dict()

        if type(script) == str:
            _script_pathlike_str_validation_check(script)

            self._script_path = script
            self._primitive_script = load(self._script_path)

            self._dict_or_list_style_script_process(self._primitive_script)

        elif type(script) == list:
            self._dict_or_list_style_script_process(script)

    def _dict_or_list_style_script_process(self, script: dict | list) -> None:
        if type(script[-1]) not in (int, list, tuple):
            raise ValueError("Frame Information is not given.")

        middle_script = dict()

        if type(script[-1]) == int:  # Mutant 1
            middle_script[0] = {
                IMAGE_INFO: self._image_info_process(script[0], 0)
            }
            
            for idx, image in enumerate(script[:-1]):
                middle_script[script[-1] * idx + 1] = {
                    IMAGE_INFO: self._image_info_process(image, idx)
                }

            middle_script[script[-1] * (len(script) - 1)] = {
                IMAGE_INFO: self._image_info_process(script[-2], len(script) - 1)
            }

        elif type(script[-1]) in (list, tuple): # Mutant 2
            frame_length_info = script[-1]

            if type(frame_length_info) not in (list, tuple):
                raise TypeError("frame length info must be list or tuple type containing the numbers, which is equal to the number of image, of positive int values.")
            if len(frame_length_info) != len(script) - 1:
                raise ValueError("frame length info must be list or tuple type containing the numbers, which is equal to the number of image, of positive int values.")
            for frame_length in frame_length_info:
                if type(frame_length) != int:
                    raise ValueError("frame length info must be list or tuple type containing the numbers, which is equal to the number of image, of positiveint values.")
                if frame_length <= 0:
                    raise ValueError("frame length info must be list or tuple type containing the numbers, which is equal to the number of image, of positiveint values.")
            
            middle_script[0] = {
                IMAGE_INFO: self._image_info_process(script[0], 0)
            }
            acc_sum = 0

            for idx, image in enumerate(script[:-1]):
                middle_script[acc_sum + 1] = {
                    IMAGE_INFO: self._image_info_process(image, idx)
                }

                acc_sum += frame_length_info[idx]

            middle_script[acc_sum] = {
                IMAGE_INFO: self._image_info_process(script[-2], len(script) - 1)
            }

        print(middle_script)

        self._final_script = keyframe_normal_to_normal_normal(middle_script, self._debugging)
        self._total_frame = len(self._final_script)

    def _image_info_process(self, image_info: dict | str | pygame.Surface, idx: int) -> dict:
        if type(image_info) not in (dict, str, pygame.Surface):
            raise TypeError(f"Image info must be Python dict, path-like str, or pygame.Surface in index {idx}.")
        
        if type(image_info) == dict:
            # Checking TARGET . . .
            if TARGET not in image_info.keys():
                raise KeyError(f"'target' key is missing in 'image_info' key in in index {idx}.")
            if type(image_info[TARGET]) not in (pygame.Surface, str):
                raise TypeError(f"Type of value in 'target' key must be pygame.Surface or path-like str in index {idx}.")
            
            if type(image_info[TARGET]) == str:
                if not os.path.exists(image_info[TARGET]): 
                    raise ValueError(f"Invalid image path in index {idx}.")
                
            # Checking RECT . . .
            if RECT not in image_info.keys():
                raise KeyError(f"'rect' key is missing in 'image_info' key in index {idx}.")
            if type(image_info[RECT]) not in (pygame.Rect, list, tuple, types.NoneType, int):
                raise TypeError(f"Type of value in 'rect' key must be pygame.Rect, list, tuple, NoneType, or int in index {idx}.")
            
            if type(image_info[RECT]) == int:
                if image_info[RECT] != 0:
                    raise ValueError(f"If the type of value in 'rect' key in 'image_info' is int, the value must be 0 in index {idx}.")

            elif type(image_info[RECT]) in (list, tuple):
                if len(image_info[RECT]) != 4:
                    raise ValueError(f"Invaild rect-style object in index {idx} -> 'rect' key.")
                
                for i in image_info[RECT]:
                    if type(image_info[RECT][i]) not in (int, float):
                        raise TypeError(f"Invaild rect-style object in index {idx} -> 'rect' key.")

            return 

        elif type(image_info) == str:
            if not os.path.exists(image_info):
                raise ValueError("Invalid image path.")

            return {
                TARGET: pygame.image.load(image_info),
                RECT: None
            }

        elif type(image_info) == pygame.Surface:
            return {
                TARGET: image_info,
                RECT: None
            }
        
    def get_total_frame(self):
        return self._total_frame

    def __str__(self) -> str:
        return str(self._final_script)

    def __repr__(self) -> str:
        return str(self._final_script)

    def __getitem__(self, key: int) -> dict:
        return self._final_script[key]
    
__all__ = [
    "SpriteAnimationScript"
]
    
if __name__ == "__main__":
    sprite_animation_script = [
        pygame.Surface((30, 30)),
        pygame.Surface((50, 50)),
        (10, 20)
    ]
    final_script = SpriteAnimationScript(sprite_animation_script)
    print(final_script)