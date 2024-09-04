import os

from pyganimation._constants import JSON

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

__all__ = [
    "_script_pathlike_str_validation_check",
    "_coordinate_validation_check",
    "_color_validation_check"
]