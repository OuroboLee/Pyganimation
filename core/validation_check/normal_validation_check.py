import os, pygame, types

from pyganimation._constants import *
from pyganimation.core.validation_check.component_validation_check import *

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
            
def _normal_normal_frame_validation_check(frame: dict) -> tuple[bool, str]:
    keys = frame.keys()
    if IMAGE_INFO not in keys:
        return False, IMAGE_INFO
    
    if not _image_info_validation_check(frame[IMAGE_INFO]):
        return False, IMAGE_INFO
    
    if POS not in keys:
        return False, POS
    
    if not _coordinate_validation_check(frame[POS]):
        return False, POS
    
    if ANGLE not in keys:
        return False, ANGLE
    
    if type(frame[ANGLE]) not in (int, float):
        return False, ANGLE
    
    if SCALE not in keys:
        return False, SCALE
    
    if not _coordinate_validation_check(frame[SCALE]):
        return False, SCALE
    
    if ALPHA not in keys:
        return False, ALPHA
    
    if type(frame[ALPHA]) not in (int, float):
        return False, ALPHA
    
    if ANGLE_ANCHOR not in keys:
        return False, ANGLE_ANCHOR
    
    if frame[ANGLE_ANCHOR] not in ANCHOR_LIST:
        return False, ANGLE_ANCHOR
    
    if SCALE_ANCHOR not in keys:
        return False, SCALE_ANCHOR
    
    if frame[SCALE_ANCHOR] not in ANCHOR_LIST:
        return False, SCALE_ANCHOR
    
    return True

def _normal_normal_validation_check(script: dict) -> bool:
    pass


__all__ = [
    "_image_info_validation_check",
    "_normal_normal_validation_check"
]
