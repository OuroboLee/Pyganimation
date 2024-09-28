import types

from pyganimation.core.validation_check.component_validation_check import *
from pyganimation._constants import ABS_POS, ABS_FLIP, ABS_ALPHA

def _frame_number_validation_check(number: int, total_frame: int) -> bool:
    if type(number) not in (int, types.NoneType):
        return False

    if type(number) == int:
        if number <= 0 or number > total_frame - 1:
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

##### Animation Info #####

def _normal_animation_info_validation_check(animation_info: dict) -> bool:
    if type(animation_info) != dict: 
        return False
    
    if ABS_POS not in animation_info.keys():
        return False
    
    if not _coordinate_validation_check(animation_info[ABS_POS]):
        return False
    
    if ABS_FLIP not in animation_info.keys():
        return False
    
    for i in range(2):
        if type(animation_info[ABS_FLIP][i]) != bool:
            return False
    
    if ABS_ALPHA not in animation_info.keys():
        return False
    
    if type(animation_info[ABS_ALPHA]) not in (int, float):
        return False
    
    return True

def _vector_animation_info_validation_check(animation_info: dict) -> bool:
    if not _normal_animation_info_validation_check(animation_info):
        return False
    
    return True

__all__ = [
    "_frame_number_validation_check",
    "_speed_validation_check",
    "_loop_validation_check",
    "_boolean_validation_check",
    "_normal_animation_info_validation_check",
    "_vector_animation_info_validation_check"
]