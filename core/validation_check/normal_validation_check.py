import os, pygame, types

from pyganimation._constants import TARGET, RECT
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

__all__ = [
    "_image_info_validation_check"
]
