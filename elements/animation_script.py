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

from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface, IAnimationTimelineInterface, IAnimationListInterface, ISpriteAnimationScriptInterface
from pyganimation.core.animation_file_manager import load
from pyganimation.core.script_converter import keyframe_normal_to_normal_normal, keyframe_vector_to_normal_vector
from pyganimation._constants import *

import os, types
import pprint

JSON = ".json"

##### Check Functions #####

def _pathlike_str_validation_check(script: str) -> None:
    assert os.path.exists(script), "Invalid path."
    assert os.path.splitext(script)[1] == JSON, "Target file must be json file."

def _coordinate_validation_check(value: list | tuple, key: str, frame_num: int, is_keyframe: bool) -> None:
    if is_keyframe:
        assert type(value) in (list, tuple), f"Invaild coordinate-style object in 'keyframe_normal_info' -> '{key}' in No.{frame_num} frame."
        assert len(value) == 2, f"Invaild coordinate-style object in 'keyframe_normal_info' -> '{key}' in No.{frame_num} frame."

        for i in range(2):
            assert type(value[i]) in (int, float), f"Invaild coordinate-style object in 'keyframe_normal_info' -> '{key}' in No.{frame_num} frame."
            
    else:
        assert type(value) in (list, tuple), f"Invaild coordinate-style object in '{key}' in No.{frame_num} frame."
        assert len(value) == 2, f"Invaild coordinate-style object in '{key}' in No.{frame_num} frame."

        for i in range(2):
            assert type(value[i]) in (int, float), f"Invaild coordinate-style object in '{key}' in No.{frame_num} frame."

def _color_validation_check(value: list | tuple, frame_num: int, is_keyframe: bool) -> None:
    if is_keyframe:
        assert type(value) in (list, tuple), f"Invalid color-style object in 'keyframe_normal_info' -> 'color' in No.{frame_num} frame."
        assert len(value) == 3, f"Invalid color-style object in 'keyframe_normal_info' -> 'color' in No.{frame_num} frame."

        for i in range(3):
            assert type(value[i]) in (int, float), f"Invalid color-style object in 'keyframe_normal_info' -> 'color' in No.{frame_num} frame."
            assert value[i] >= 0 and value[i] < 255, f"Invalid color-style object in 'keyframe_normal_info' -> 'color' in No.{frame_num} frame." 

    else:
        assert type(value) in (list, tuple), f"Invalid color-style object in 'color' in No.{frame_num} frame."
        assert len(value) == 3, f"Invalid color-style object in 'color' in No.{frame_num} frame."

        for i in range(3):
            assert type(value[i]) in (int, float), f"Invalid color-style object in 'color' in No.{frame_num} frame."
            assert value[i] >= 0 and value[i] < 255, f"Invalid color-style object in 'color' in No.{frame_num} frame." 

##### Vector #####




##### Main #####

class AnimationScript(IAnimationScriptInterface):
    def __init__(self,
                 script: str | dict[dict] | list[dict],
                 debugging: bool = False):
        assert type(script) in (str, dict, list), "Script Parameter must be among path-like str that represents json format file, Python dict, or Python list."

        self.debugging = debugging

        self._primitive_script = None
        self._script_path = None
        
        self._final_script = dict()

        if type(script) == str:
            _pathlike_str_validation_check(script)

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
                    self._keyframe_normal_script_validation_check(script)
                    self._final_script = keyframe_normal_to_normal_normal(script, self.debugging)


                elif SHAPE_INFO in script[0].keys(): # Vector
                    self._script_type = SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION
                    self._keyframe_vector_script_validation_check(script, self.debugging)

            else: # Normal
                assert len(script) == list(script.keys())[-1] + 1, "There is a frame that is not given in Normal Animation Script."

                if IMAGE_INFO in script[0].keys(): # Normal
                    self._script_type = SCRIPTTYPE_NORMAL_NORMAL_ANIMATION
                    self._normal_normal_script_validation_check(script)
                    self._final_script = script.copy()


                elif SHAPE_INFO in script[0].keys(): # Vector
                    self._script_type = SCRIPTTYPE_NORMAL_VECTOR_ANIMATION
                    self._normal_vector_script_validation_check(script)

        

        elif type(script) == list: # Only Normal Animation Script 
            if IMAGE_INFO in script[0].keys():
                self._normal_normal_script_validation_check(script, self.debugging)
            elif SHAPE_INFO in script[0].keys():
                self._normal_vector_script_validation_check(script, self.debugging)
                
    def _normal_normal_script_validation_check(self, script: dict | list): # For dict-style / list-style normal normal script.
        if type(script) == dict:
            new_script = script.copy()
        elif type(script) == list:
            new_script == {x: script[x] for x in range(len(script))}

        for frame_num, frame in new_script.items():
            assert IMAGE_INFO in frame.keys(), f"'image_information' key is missing in No.{frame_num} frame."
            self._image_info_validation_check(frame[IMAGE_INFO], frame_num)

            normal_info = frame.copy()
            normal_info.pop(IMAGE_INFO)

            self._normal_normal_info_validation_check(normal_info, frame_num)
                

    def _keyframe_normal_script_validation_check(self, script: dict): # For dict-style keyframe normal script
        for frame_num, frame in script.items():
            if frame_num == 0:
                assert IMAGE_INFO in frame.keys(), f"'image_information' key is missing in No.{frame_num} frame."
                self._image_info_validation_check(frame[IMAGE_INFO], frame_num)

                assert KEYFRAME_NORMAL_INFO in frame.keys(), f"'keyframe_normal_info' key is missing in No.{frame_num} frame."
                self._keyframe_normal_info_validation_check(frame[KEYFRAME_NORMAL_INFO], frame_num)


            else: 
                if IMAGE_INFO in frame.keys():
                    self._image_info_validation_check(frame[IMAGE_INFO], frame_num)
                
                if KEYFRAME_NORMAL_INFO in frame.keys():
                    self._keyframe_normal_info_validation_check(frame[KEYFRAME_NORMAL_INFO], frame_num)

                    if KEYFRAME_INTERPOLATE_INFO in frame.keys():
                        pass

    def _normal_vector_script_validation_check(self, script: dict | list): # For dict-style / list-style normal vector script.
        if type(script) == dict:
            new_script = script.copy()
        elif type(script) == list:
            new_script = {x: script[x] for x in range(len(script))}

        for frame_num, frame in new_script.items():
            assert SHAPE_INFO in frame.keys(), f"'shape_information' key is missing in No.{frame_num} frame."
            self._shape_info_validation_check(frame[SHAPE_INFO], frame_num)

    def _keyframe_vector_script_validation_check(self, script: dict): # For dict-style keyframe vector script
        for frame_num, frame in script.items():
            if frame_num == 0:
                assert SHAPE_INFO in frame.keys(), f"'shape_information' key is missing in No.{frame_num} frame."
                self._shape_info_validation_check(frame[SHAPE_INFO])
            
            else:
                pass

    @staticmethod
    def _image_info_validation_check(image_info: dict, frame_num: int) -> None:
        assert TARGET in image_info.keys(), f"'target' key is missing in 'image_info' key in No.{frame_num} frame."
        assert type(image_info[TARGET]) in (pygame.Surface, str), f"Type of value in 'target' key must be pygame.Surface or path-like str in No.{frame_num} frame."
        if type(image_info[TARGET]) == str:
            assert os.path.exists(image_info[TARGET]), f"Invalid image path in No.{frame_num} frame."

        assert RECT in image_info.keys(), f"'rect' key is missing in 'image_info' key in No.{frame_num} frame."
        assert type(image_info[RECT]) in (pygame.Rect, list, tuple, types.NoneType, int), f"Type of value in 'rect' key must be pygame.Rect, list, tuple, NoneType, or int in in No.{frame_num} frame."

        if type(image_info[RECT]) == int:
            assert image_info[RECT] == 0, f"If the type of value in 'rect' key in 'image_info' is int, the value must be 0 in No.{frame_num} frame."

        elif type(image_info[RECT]) in (list, tuple):
            assert len(image_info[RECT]) == 4, f"Invaild rect-style object in No.{frame_num} frame."
            for i in image_info[RECT]:
                assert type(image_info[RECT][i]) in (int, float), f"Invaild rect-style object in No.{frame_num} frame."

    @staticmethod
    def _shape_info_validation_check(shape_info: dict, frame_num: int) -> None:
        assert TARGET in shape_info.keys(), f"'target' key is missing in No.{frame_num} frame."
        assert shape_info[TARGET] in SHAPE_LIST, f"Invaild shape target in No.{frame_num} frame."
        assert INFO in shape_info.keys(), f"'info' key is missing in No.{frame_num} frame."

        if shape_info[TARGET] in (ELLIPSE, RECTANGLE):
            assert type(shape_info[INFO]) in (Rect, tuple, list, types.NoneType), f"Invalid shape info in No.{frame_num} frame."

            if type(shape_info[INFO]) in (tuple, list):
                assert len(shape_info[INFO]) in (2, 4), f"Invalid shape info in No.{frame_num} frame."

                if len(shape_info[INFO]) == 2: # (top, left, width, height)
                    for i in range(4):
                        assert type(shape_info[INFO][i]) in (int, float), f"Invalid shape info in No.{frame_num} frame."
                    
                else: # (width, height)
                    for i in range(2):
                        assert type(shape_info[INFO][i]) in (int, float), f"Invalid shape info in No.{frame_num} frame."

        elif shape_info[TARGET] in (SQUARE, CIRCLE):
            assert type(shape_info[INFO]) in (int, float, types.NoneType), f"Invalid shape info in No.{frame_num} frame."



        elif shape_info[TARGET] == ARC:
            pass

        elif shape_info[TARGET] == PIE:
            pass

        elif shape_info[TARGET] == LINE:
            pass

        elif shape_info[TARGET] == LINES:
            pass
        
        elif shape_info[TARGET] == BEZIER:
            pass


    @staticmethod
    def _normal_normal_info_validation_check(normal_info: dict, frame_num: int) -> None:
        # POS
        assert POS in normal_info.keys(), f"'pos' key is missing in No.{frame_num} frame."
        _coordinate_validation_check(normal_info[POS], POS, frame_num, False)

        # ANGLE
        assert ANGLE in normal_info.keys(), f"'angle' key is missing in No.{frame_num} frame."
        assert type(normal_info[ANGLE]) in (int, float), f"Invalid angle value 'angle' in No.{frame_num} frame."

        # SCALE
        assert SCALE in normal_info.keys(), f"'scale' key is missing in No.{frame_num} frame."
        _coordinate_validation_check(normal_info[SCALE], SCALE, frame_num, False)

        # ALPHA
        assert ALPHA in normal_info.keys(), f"'alpha' key is missing in No.{frame_num} frame."
        assert type(normal_info[ALPHA]) in (int, float), f"Invalid alpha value in 'alpha' in No.{frame_num} frame."
        assert normal_info[ALPHA] >= 0 and normal_info[ALPHA] <= 255, f"Invalid alpha value in 'alpha' in No.{frame_num} frame."
    
    @staticmethod
    def _keyframe_normal_info_validation_check( normal_info: dict, frame_num: int) -> None:
        if frame_num == 0:
            # POS
            assert POS in normal_info.keys(), f"'pos' key is missing in No.{frame_num} frame -> 'keyframe_normal_info'."
            _coordinate_validation_check(normal_info[POS], POS, frame_num, True)

            # ANGLE
            if ANGLE in normal_info.keys():
                assert type(normal_info[ANGLE]) in (int, float), f"Invalid angle value in 'keyframe_normal_info' -> 'angle' in No.{frame_num} frame."

            # SCALE
            if SCALE in normal_info.keys():
                _coordinate_validation_check(normal_info[SCALE], SCALE, frame_num, True)

            # ALPHA
            if ALPHA in normal_info.keys():
                assert type(normal_info[ALPHA]) in (int, float), f"Invalid alpha value in 'keyframe_normal_info' -> 'alpha' in No.{frame_num} frame."
                assert normal_info[ALPHA] >= 0 and normal_info[ALPHA] <= 255, f"Invalid alpha value in 'keyframe_normal_info' -> 'alpha' in No.{frame_num} frame."
        else:
            # POS
            if POS in normal_info.keys():
                _coordinate_validation_check(normal_info[POS], POS, frame_num, False)
            
            # ANGLE
            if ANGLE in normal_info.keys(): 
                assert type(normal_info[ANGLE]) in (int, float), f"Invalid angle value in 'keyframe_normal_info' -> 'angle' in No.{frame_num} frame."

            # SCALE
            if SCALE in normal_info.keys():
                _coordinate_validation_check(normal_info[SCALE], SCALE, frame_num, False)

            # ALPHA
            if ALPHA in normal_info.keys(): 
                assert type(normal_info[ALPHA]) in (int, float), f"Invalid alpha value in 'keyframe_normal_info' -> 'alpha' in No.{frame_num} frame."
                assert normal_info[ALPHA] >= 0 and normal_info[ALPHA] <= 255, f"Invalid alpha value in 'keyframe_normal_info' -> 'alpha' in No.{frame_num} frame."

    @staticmethod
    def _keyframe_normal_interpolate_info_validation_check(normal_info: dict, interpol_info: dict, frame_num: int) -> None:
        if POS in interpol_info.keys():
            assert POS in normal_info.keys(), f"Interpolate Function for 'pos' was given while value was not given in 'keyframe_normal_info in No.{frame_num} frame."

            assert type(interpol_info[POS]) in (str, list, tuple), f"Invalid interpolate function type in 'keyframe_interpolate_info' -> 'pos' in No.{frame_num} frame."
            if type(interpol_info[POS]) == str:
                assert interpol_info[POS] in INTERPOLATE_FUNC_LIST, f"Invalid interpolate function in 'keyframe_interpolate_info' -> 'pos' in No.{frame_num} frame."
            
            elif type(interpol_info[POS]) in (list, tuple):
                for i in range(2):
                    assert interpol_info[POS][i] in INTERPOLATE_FUNC_LIST, f"Invalid interpolate function in 'keyframe_interpolate_info' -> 'pos' in No.{frame_num} frame."

        if ANGLE in interpol_info.keys():
            assert ANGLE in normal_info.keys(), f"Interpolate Function for 'angle' was given while value was not given in 'keyframe_normal_info in No.{frame_num} frame."

            assert interpol_info[ANGLE] in INTERPOLATE_FUNC_LIST, f"Invalid interpolate function in 'keyframe_interpolate_info' -> 'angle' in No.{frame_num} frame."

        if SCALE in interpol_info.keys():
            assert type(interpol_info[SCALE]) in (str, list, tuple), f"Invalid interpolate function type in 'keyframe_interpolate_info' -> 'scale' in No.{frame_num} frame."
            if type(interpol_info[SCALE]) == str:
                assert interpol_info[SCALE] in INTERPOLATE_FUNC_LIST, f"Invalid interpolate function in 'keyframe_interpolate_info' -> 'scale' in No.{frame_num} frame."

            elif type(interpol_info[SCALE]) in (list, tuple):
                for i in range(2):
                    assert interpol_info[POS][i] in INTERPOLATE_FUNC_LIST, f"Invalid interpolate function in 'keyframe_interpolate_info' -> 'scale' in No.{frame_num} frame."

        if SCALE_ANCHOR in interpol_info.keys():
            assert interpol_info[SCALE_ANCHOR] in SCALE_ANCHOR_LIST, f"Invalid scale anchor in 'keyframe_interpolate_info' -> 'scale_anchor' in No.{frame_num} frame."

        if ALPHA in interpol_info.keys():
            assert interpol_info[ALPHA] in INTERPOLATE_FUNC_LIST, f"Invalid interpolate function in 'keyframe_interpolate_info' -> 'alpha' in No.{frame_num} frame."

    def _keyframe_vector_info_validation_check(keyframe_info: dict, shape_target: str, frame_num: int) -> types.NoneType:
        pass

    def _normal_vector_info_validation_check(normal_info: dict, shape_target: str, frame_num: int) -> types.NoneType:
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
    
class SpriteAnimationScript(ISpriteAnimationScriptInterface):
    def __init__(self,
                 script: list | str,
                 debugging: bool = False
                 ):
        self._script_path = None
        self._primitive_script = None

        self._final_script = dict()

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def __getitem__(self, key: int) -> dict:
        pass

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
            _pathlike_str_validation_check(script)

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
    
class AnimationTimeline(IAnimationTimelineInterface):
    def __init__(self,
                 script: list | dict | str,
                 debugging: bool = False
                ):
        """
        """
        assert type(script) in (list, dict, str), "Script Parameter must be among path-like str that represents json format file, Python dict, or Python list."

        self._primitive_script = None
        self._script_path = None
        self._debugging = debugging

        if type(script) == str:
            _pathlike_str_validation_check(script)
            
            self._script_path = script
            self._primitive_script = load(script)
        
        else:
            pass
        
        
        self._final_script = dict()





        self._total_frame = 0

    def get_total_frame(self):
        return self._total_frame
    
    def set_total_frame(self, value: int):
        if self._total_frame == 0:
            self._total_frame = value

    def _script_validation_check(self):
        pass

    def timeline_validation_check(self, animation_list: IAnimationListInterface):
        pass

    def __str__(self) -> str:
        return f"<AnimationTimeline Object (Total Frame: {self._total_frame}))>"
    
    def __repr__(self) -> str:
        return pprint.pformat(self._final_script, 4, 300)
    
    def __getitem__(self, key: int) -> dict:
        return self._final_script[key]
    
__all__ = [
    "AnimationScript",
    "AnimationTimeline",
    "AnimationList",
    "SpriteAnimationScript"
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
