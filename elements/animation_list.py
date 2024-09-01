from pyganimation.core.script_validation_check import *
from pyganimation.core.animation_list_converter import list_to_default, dict_to_default
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

        self._final_script = dict()

        if type(script) == str:
            _script_pathlike_str_validation_check(script)

            self._script_path = script
            self._primitive_script = load(script)

            self._dict_or_list_style_script_process(self._primitive_script)

        else:
            self._dict_or_list_style_script_process(script)

    def _dict_or_list_style_script_process(self, script: dict | list) -> types.NoneType:
        if type(script) == list:
            self._final_script = list_to_default(script)

        elif type(script) == dict:
            self._final_script = dict_to_default(script)

    def get_name_list(self) -> list[str]:
        result_list = list()
        for name in self._final_script.keys():
            result_list.append(name)

        return result_list

    def __str__(self) -> str:
        return f"AnimationList object with {len(self._final_script)} contents."

    def __repr__(self) -> str:
        return pprint.pformat(self._final_script, 4, 300)

    def __len__(self) -> int:
        return len(self._final_script)
 
    def __getitem__(self, key: str) -> dict:
        return self._final_script[key]
    
if __name__ == "__main__":
    from pyganimation._constants import *
    from pyganimation import AnimationScript
    import pygame

    example_keyframe_script = {
        0: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((50, 50)),
                RECT: None
            },
            KEYFRAME_NORMAL_INFO: {
                POS: (400, 400)
            }
        },
        1: {
            KEYFRAME_NORMAL_INFO: {
                POS: (400, 400)
            }
        },
        60: {
            KEYFRAME_NORMAL_INFO: {
                POS: (500, 500),
                ANGLE: 0
            },
            KEYFRAME_INTERPOLATE_INFO: {
                POS: SIN_IN_AND_OUT,
                ANGLE: SIN_IN_AND_OUT
            }
        }
    }
    example_script = AnimationScript(example_keyframe_script)
    test_script = {
        "example1": {
            ANIMATION_SCRIPT: example_script
        },
        "example2": {
            ANIMATION_SCRIPT: example_script,
            ANIMATION_PARAM_INFO: {
                SPEED: 2,
                LOOP: -1,
                ANIMATION_INFO: {
                    ABS_POS:(500, 0),
                    ABS_ANGLE: 0,
                    ABS_SCALE: (1, 1),
                    ABS_ALPHA: 1
                }
            }
        }
    }
    test = AnimaitionList(test_script)

    print(repr(test))