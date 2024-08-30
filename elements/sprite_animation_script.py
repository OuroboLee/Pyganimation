from pyganimation.core.script_validation_check import *
from pyganimation.core.interface.animation_script_interface import ISpriteAnimationScriptInterface
from pyganimation.core.animation_file_manager import load
from pyganimation._constants import *

import pygame
import pprint, types, os

class SpriteAnimationScript(ISpriteAnimationScriptInterface):
    def __init__(self,
                 script: list[dict] | str,
                 debugging: bool = False
                 ):
        if type(script) not in (list, str):
            raise TypeError("Script parameter must be among path-like str that represents json format file or Python list.")

        self._debugging = debugging

        self._script_path = None
        self._primitive_script = None

        self._final_script = dict()

        if type(script) == str:
            _script_pathlike_str_validation_check(script)

            self._script_path = script
            self._primitive_script = load(self._script_path)

            self._dict_or_list_style_script_process(self._primitive_script)

        elif type(script) == list:
            self._dict_or_list_style_script_process(script)

    def _dict_or_list_style_script_process(self, script: dict | list) -> None:
        
        if type(script[-1]) == int:  # Mutant 1
            pass

        elif type(script[-1]) in (list, tuple): # Mutant 2
            pass

    def _image_info_validation_check(self, image_info: dict | str | pygame.Surface, idx: int) -> dict:
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

        elif type(image_info) == str:
            _script_pathlike_str_validation_check(image_info, idx)

            return {
                TARGET: pygame.image.load(image_info),
                RECT: None
            }

        elif type(image_info) == pygame.Surface:
            return {
                TARGET: image_info,
                RECT: None
            }

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def __getitem__(self, key: int) -> dict:
        return self._final_script[key]