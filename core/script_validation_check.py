import os, types, pygame

from pyganimation._constants import *

JSON = ".json"

##### Check Functions #####

def _script_pathlike_str_validation_check(script: str, idx: int | types.NoneType = None) -> None:
    if idx is not None:
        if not os.path.exists(script):
            raise ValueError("Invalid path.")
        if os.path.splitext(script)[1] != JSON:
            raise ValueError("Target file must be json file.")
    else:
        if not os.path.exists(script):
            raise ValueError(f"Invalid path in index {idx}.")
        if os.path.splitext(script)[1] != JSON:
            raise ValueError(f"Target file must be json file in index {idx}.")

def _coordinate_validation_check(value: list | tuple, key: str, frame_num: int, is_keyframe: bool) -> None:
    if is_keyframe:
        if type(value) not in (list, tuple):
            raise TypeError(f"Invaild coordinate-style object in 'keyframe_normal_info' -> '{key}' in No.{frame_num} frame.")
        if len(value) != 2: 
            raise ValueError(f"Invaild coordinate-style object in 'keyframe_normal_info' -> '{key}' in No.{frame_num} frame.")

        for i in range(2):
            if type(value[i]) not in (int, float):
                raise ValueError(f"Invaild coordinate-style object in 'keyframe_normal_info' -> '{key}' in No.{frame_num} frame.")
            
    else:
        if type(value) not in (list, tuple):
            raise TypeError(f"Invaild coordinate-style object in '{key}' in No.{frame_num} frame.")
        if len(value) != 2:
            raise ValueError(f"Invaild coordinate-style object in '{key}' in No.{frame_num} frame.")

        for i in range(2):
            if type(value[i]) not in (int, float):
                raise ValueError(f"Invaild coordinate-style object in '{key}' in No.{frame_num} frame.")

def _color_validation_check(value: list | tuple, frame_num: int, is_keyframe: bool) -> None:
    if is_keyframe:
        if type(value) not in (list, tuple):
            raise TypeError(f"Invalid color-style object in 'keyframe_normal_info' -> 'color' in No.{frame_num} frame.")
        if len(value) != 3:
            raise ValueError(f"Invalid color-style object in 'keyframe_normal_info' -> 'color' in No.{frame_num} frame.")

        for i in range(3):
            if type(value[i]) not in (int, float):
                raise ValueError(f"Invalid color-style object in 'keyframe_normal_info' -> 'color' in No.{frame_num} frame.")

    else:
        if type(value) not in (list, tuple):
            raise TypeError(f"Invalid color-style object in 'color' in No.{frame_num} frame.")
        if len(value) != 3:
            raise ValueError(f"Invalid color-style object in 'color' in No.{frame_num} frame.")

        for i in range(3):
            if type(value[i]) not in (int, float):
                raise ValueError(f"Invalid color-style object in 'color' in No.{frame_num} frame.")
            
##### Normal Animation Check Functions #####

def _image_info_validation_check(image_info: dict, frame_num: int):
    if TARGET not in image_info.keys():
        raise KeyError(f"'target' key is missing in 'image_info' key in No.{frame_num} frame.")
    
    if type(image_info[TARGET]) not in (pygame.Surface, str):
        raise TypeError(f"Type of value in 'target' key must be pygame.Surface or path-like str in No.{frame_num} frame.")
    if type(image_info[TARGET]) == str:
        if not os.path.exists(image_info[TARGET]):
            raise ValueError(f"Invalid image path in No.{frame_num} frame.")

    if RECT not in image_info.keys():
        raise KeyError(f"'rect' key is missing in 'image_info' key in No.{frame_num} frame.")
    if type(image_info[RECT]) not in (pygame.Rect, list, tuple, types.NoneType, int):
        raise TypeError(f"Type of value in 'rect' key must be pygame.Rect, list, tuple, NoneType, or int in in No.{frame_num} frame.")

    if type(image_info[RECT]) == int:
        if image_info[RECT] != 0:
            raise ValueError(f"If the type of value in 'rect' key in 'image_info' is int, the value must be 0 in No.{frame_num} frame.")

    elif type(image_info[RECT]) in (list, tuple):
        if len(image_info[RECT]) != 4:
            raise ValueError(f"Invaild rect-style object in No.{frame_num} frame.")
        for i in image_info[RECT]:
            if type(image_info[RECT][i]) not in (int, float):
                raise ValueError(f"Invaild rect-style object in No.{frame_num} frame.")

##### Vector Animation Check Functions #####

def _shape_info_validation_check(shape_info: dict, frame_num: int):
    pass

##### Parameter Check Functions #####

def _normal_animation_info_validation_check(animation_info: dict):
    if type(animation_info) != dict: return False
    if ABS_POS not in animation_info.keys():
        return False
    pass


__all__ = [
    "_script_pathlike_str_validation_check",
    "_coordinate_validation_check",
    "_color_validation_check",
    "_image_info_validation_check",
    "_shape_info_validation_check"
]