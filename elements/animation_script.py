# AnimationScript class.
#
# Adding Instructions...
#
# AnimationList class.
#
# Adding Instructions...
#
# AnimationTimeline class.
#
# Adding Instructions...
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

from pygame import Rect

from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface
from pyganimation.core.script_validation_check import *
from pyganimation.core.animation_file_manager import load
from pyganimation.core.converter.script_converter import keyframe_normal_to_normal_normal, keyframe_vector_to_normal_vector
from pyganimation._constants import *

import os, types
import pprint

##### Main #####

class AnimationScript(IAnimationScriptInterface):
    def __init__(self,
                 script: str | dict[dict] | list[dict],
                 debugging: bool = False):
        assert type(script) in (str, dict, list), "Script parameter must be among path-like str that represents json format file, Python dict, or Python list."

        self.debugging = debugging

        self._primitive_script = None
        self._script_path = None
        
        self._final_script = dict()

        if type(script) == str:
            _script_pathlike_str_validation_check(script)

            self._script_path = script
            self._primitive_script = load(self._script_path)

            first_processed_script = dict()
            for key, value in self._primitive_script.items():
                first_processed_script[int(key)] = value
            
            self._dict_or_list_style_script_process(first_processed_script)
        else:
            self._dict_or_list_style_script_process(script)


    def _dict_or_list_style_script_process(self, script: dict | list) -> types.NoneType:
        if type(script) == dict:
            assert list(script.keys())[0] == 0, "Dict-style Animation Script must have No.0 frame."
            if KEYFRAME_NORMAL_INFO in script[0].keys(): # Keyframe
                if IMAGE_INFO in script[0].keys(): # Normal
                    self._script_type = SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION
                    self._final_script = keyframe_normal_to_normal_normal(script, self.debugging)


                elif SHAPE_INFO in script[0].keys(): # Vector
                    self._script_type = SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION
                    pass

            else: # Normal
                assert len(script) == list(script.keys())[-1] + 1, "There is a frame that is not given in Normal Animation Script."

                if IMAGE_INFO in script[0].keys(): # Normal
                    self._script_type = SCRIPTTYPE_NORMAL_NORMAL_ANIMATION
                    self._final_script = script.copy()


                elif SHAPE_INFO in script[0].keys(): # Vector
                    self._script_type = SCRIPTTYPE_NORMAL_VECTOR_ANIMATION

        

        elif type(script) == list: # Only Normal Animation Script 
            if IMAGE_INFO in script[0].keys():
                pass
            elif SHAPE_INFO in script[0].keys():
                pass

    def get_total_frame(self):
        return list(self._final_script.keys())[-1] + 1
    
    def get_script_type(self):
        return self._script_type
        
    def __str__(self) -> str:
        return f"<AnimationScript Object (Total Frame: {self.get_total_frame()}, Script Type: {self.get_script_type()})>"

    def __repr__(self) -> str:
        return pprint.pformat(self._final_script, 4, 300)
    
    def __getitem__(self, key: int) -> dict:
        return self._final_script[key]
    
__all__ = [
    "AnimationScript"
]
    
if __name__ == "__main__":
    keyframe_script = {
        0: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((50, 50)),
                RECT: None
            },
            KEYFRAME_NORMAL_INFO: {
                POS: (0, 0),
                SCALE: (1, 1),
            }
        },
        20: {
            KEYFRAME_NORMAL_INFO: {
                ALPHA: 128,
                SCALE: (0.7, 1.3)
            },
            KEYFRAME_INTERPOLATE_INFO: {
                SCALE: SIN_IN,
                SCALE_ANCHOR: TOPMID
            }
        },
        40: {
            KEYFRAME_NORMAL_INFO: {
                SCALE: (1, 1),
            },
            KEYFRAME_INTERPOLATE_INFO: {
                SCALE: SIN_IN,
                SCALE_ANCHOR: TOPMID
            }
        }
    }
    normal_script = keyframe_normal_to_normal_normal(keyframe_script)
    print(normal_script)

    script = AnimationScript(normal_script)

    print(repr(script))
