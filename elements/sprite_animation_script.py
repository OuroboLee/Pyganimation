from pyganimation.core.validation_check import *
from pyganimation.core.interface.animation_script_interface import ISpriteAnimationScriptInterface
from pyganimation.core.animation_file_manager import load
from pyganimation.core.converter.sprite_animation_script_converter import mutant1_to_final_script, mutant2_to_final_script
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

        else:
            raise ValueError("Invalid script.")

    def _dict_or_list_style_script_process(self, script: dict | list) -> None:
        if type(script[-1]) == int:  # Mutant 1
            self._final_script = mutant1_to_final_script(script, self._debugging)

        elif type(script[-1]) in (list, tuple): # Mutant 2
            self._final_script = mutant2_to_final_script(script, self._debugging)

        else:
            raise ValueError("Invalid script.")
        
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
        3
    ]
    final_script = SpriteAnimationScript(sprite_animation_script, True)
    print(final_script)