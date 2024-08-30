from pyganimation.core.script_validation_check import *
from pyganimation.core.interface.animation_script_interface import IAnimationListInterface
from pyganimation.core.animation_file_manager import load

import pprint
import types


class AnimaitionList(IAnimationListInterface):
    def __init__(self,
                 script: list | dict | str,
                 debugging: bool = False):
        assert type(script) in (list, dict, str), "Script Parameter must be among path-like str that represents json format file, Python dict, or Python list."

        self._primitive_script = None
        self._script_path = None

        self._debugging = debugging

        self._final_script = list()

        if type(script) == str:
            _script_pathlike_str_validation_check(script)

            self._script_path = script
            self._primitive_script = load(script)

            self._dict_or_list_style_script_process(self._primitive_script)

        else:
            self._dict_or_list_style_script_process(script)

    def _dict_or_list_style_script_process(self, script: dict | list) -> types.NoneType:
        if type(script) == list:
            pass

        elif type(script) == dict:
            pass

    def get_name_list(self) -> list[str]:
        result_list = list()
        for anim in self._final_script:
            result_list.append(anim.animation_name)

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def __len__(self) -> int:
        return len(self._final_script)
 
    def __getitem__(self, key: str) -> dict:
        pass