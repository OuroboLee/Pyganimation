import os, types, pygame

from pyganimation._constants import *
from pyganimation.core.interface import IAnimationScriptInterface

JSON = ".json"

##### Check Functions #####

def _script_pathlike_str_validation_check(script: str) -> bool:
    if not os.path.exists(script):
        return False
    if os.path.splitext(script)[1] != JSON:
        return False
    return True

def _coordinate_validation_check(value: list | tuple) -> bool:
    if type(value) not in (list, tuple):
        return False
    if len(value) != 2: 
        return False

    for i in range(2):
        if type(value[i]) not in (int, float):
            return False
            
    return True

def _color_validation_check(value: list | tuple) -> bool:
    if type(value) not in (list, tuple):
        return False
    if len(value) != 3:
        return False

    for i in range(3):
        if type(value[i]) not in (int, float):
            return False
    
    return True
            
##### Normal Animation Check Functions #####

def _image_info_validation_check(image_info: dict) -> bool:
    if TARGET not in image_info.keys():
        return False
    
    if type(image_info[TARGET]) not in (pygame.Surface, str):
        return False
    if type(image_info[TARGET]) == str:
        if not os.path.exists(image_info[TARGET]):
            return False

    if RECT not in image_info.keys():
        return False
    if type(image_info[RECT]) not in (pygame.Rect, list, tuple, types.NoneType, int):
        return False

    if type(image_info[RECT]) == int:
        if image_info[RECT] != 0:
            return False

    elif type(image_info[RECT]) in (list, tuple):
        if len(image_info[RECT]) != 4:
            raise False
        for i in image_info[RECT]:
            if type(image_info[RECT][i]) not in (int, float):
                raise False

##### Vector Animation Check Functions #####

def _shape_info_validation_check(shape_info: dict) -> bool:
    pass

##### Parameter Check Functions #####

def _frame_number_validation_check(number: int, script: IAnimationScriptInterface) -> bool:
    if type(number) not in (int, types.NoneType):
        return False

    if number <= 0 or number > script.get_total_frame() - 1:
        return False
    
    return True
    
def _speed_validation_check(number: int | float) -> bool:
    if type(number) not in (int, float):
        return False
    if number <= 0:
        return False
    return True
    
def _loop_validation_check(number: int) -> bool:
    if type(number) != int:
        return False
    return True

def _boolean_validation_check(value: bool) -> bool:
    if type(value) != bool:
        return False
    return True

def _normal_animation_info_validation_check(animation_info: dict) -> bool:
    if type(animation_info) != dict: 
        return False
    
    if ABS_POS not in animation_info.keys():
        return False
    
    if not _coordinate_validation_check(animation_info[ABS_POS]):
        return False
    
    if ABS_ANGLE not in animation_info.keys():
        return False
    
    if type(animation_info[ABS_ANGLE]) not in (int, float):
        return False
    
    if ABS_SCALE not in animation_info.keys():
        return False
    
    if not _coordinate_validation_check(animation_info[ABS_SCALE]):
        return False
    
    if ABS_ALPHA not in animation_info.keys():
        return False
    
    if type(animation_info[ABS_ANGLE]) not in (int, float):
        return False
    
    return True

def _vector_animation_info_validation_check(animation_info: dict) -> bool:
    if not _normal_animation_info_validation_check(animation_info):
        return False
    
    return True

__all__ = [
    "_script_pathlike_str_validation_check",
    "_coordinate_validation_check",
    "_color_validation_check",
    "_image_info_validation_check",
    "_shape_info_validation_check",
    "_frame_number_validation_check",
    "_speed_validation_check",
    "_loop_validation_check",
    "_boolean_validation_check",
    "_normal_animation_info_validation_check",
    "_vector_animation_info_validation_check"
]