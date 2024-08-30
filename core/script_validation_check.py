import os

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

__all__ = [
    "_pathlike_str_validation_check",
    "_coordinate_validation_check",
    "_color_validation_check"
]