from pyganimation.core.script_validation_check import *
from pyganimation.core.interface.animation_script_interface import ISpriteAnimationScriptInterface
from pyganimation.core.animation_file_manager import load

import pprint

class SpriteAnimationScript(ISpriteAnimationScriptInterface):
    def __init__(self,
                 script: list | str,
                 debugging: bool = False
                 ):
        self._script_path = None
        self._primitive_script = None

        self._final_script = dict()

    
    def _dict_or_list_style_script_process(self, script: dict | list) -> None:
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def __getitem__(self, key: int) -> dict:
        pass