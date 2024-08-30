import os

JSON = ".json"

##### Check Functions #####

def _pathlike_str_validation_check(script: str) -> None:
    if not os.path.exists(script):
        raise ValueError("Invalid path.")
    if os.path.splitext(script)[1] != JSON:
        raise ValueError("Target file must be json file.")

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

__all__ = [
    "_pathlike_str_validation_check",
    "_coordinate_validation_check",
    "_color_validation_check"
]