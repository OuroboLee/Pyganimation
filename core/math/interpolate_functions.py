from math import sin, cos, radians, pi, exp
from pyganimation._constants import *

import pygame

##### TRANSFORM FUNCTIONS #####

"""
함수 제작 규칙 :

1. 각 함수는 다음 조건을 만족하는 수학적 함수를 사용해야 함.
    1) 0 이상 1 이하의 실수 범위에서 문제없이 정의되어야 함.
    2) 0과 1 사이에서의 정적분 값이 1이어야 함.
    3) 다음을 지킬 것이 권장됨.
        1> IN 형식일 때, 0에서 순간변화율 0
        2> OUT 형식일 때, 1에서 순간변화율 0
3. 각 함수는 int형의 total_frame과 int형의 frame_number인자를 반드시 받아야 함.
4. 각 함수는 최종적으로 float형의 값을 반환해야 함.

각 함수에 쓰인 수학적 함수의 각 x값에 대해 도출된 값이 키 프레임 사이의 각 프레임 간의 변화율의 가중치(=속도) 로 작용함.
"""
# linear

def linear(total_frame: int, frame_number: int) -> float:
    return 1

# sin

def sin_in_and_out_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return 0.5 * pi * sin(pi*x)

def sin_in_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return 0.5 * pi * sin(0.5*pi*x)

def sin_out_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return 0.5 * pi * sin(0.5*pi*(1-x))

# back 

BACK_COMP = 20 # Should be BACK_COMP > 4
BACK_COMP2 = -1000 # Should be BACK_COMP2 < -140
def back_in_and_out_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return BACK_COMP2 * (x ** 2) * ((x - 1) ** 2) * (((x - 0.5) ** 2) - 1 / 28 + 30 / BACK_COMP2)

def back_in_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return BACK_COMP * x ** 3 + (3 - 0.75 * BACK_COMP) * x ** 2

def back_out_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return BACK_COMP * (1 - x) ** 3 + (3 - 0.75 * BACK_COMP) * (1 - x) ** 2

# expo

EXPO_COMP = 5
def expo_in_and_out_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    """WIP"""

def expo_in_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return ((2 * EXPO_COMP) / (2 * exp(EXPO_COMP) - EXPO_COMP ** 2 - 2 * EXPO_COMP - 2)) * (exp(EXPO_COMP * x) - (EXPO_COMP * x) - 1)

def expo_out_func(total_frame: int, frame_number: int) -> float:
    x = frame_number / total_frame
    return ((2 * EXPO_COMP) / (2 * exp(EXPO_COMP) - EXPO_COMP ** 2 - 2 * EXPO_COMP - 2)) * (exp(EXPO_COMP * (1 - x)) - (EXPO_COMP * (1 - x)) - 1)

# instant

def instant_in_func(total_frame: int, frame_number: int) -> float:
    return 0

def instant_out_func(total_frame: int, frame_number: int) -> float:
    return 2 * total_frame if frame_number == 0 else 0


##############################################################

def get_func_from_interpolate_info(flag: str):
    if flag == SIN_IN:
        return sin_in_func
    elif flag == SIN_OUT:
        return sin_out_func
    elif flag == SIN_IN_AND_OUT:
        return sin_in_and_out_func
    elif flag == EXPO_IN:
        return expo_in_func
    elif flag == EXPO_OUT:
        return expo_out_func
    elif flag == EXPO_IN_AND_OUT:
        return expo_in_and_out_func
    elif flag == BACK_IN:
        return back_in_func
    elif flag == BACK_OUT:
        return back_out_func
    elif flag == BACK_IN_AND_OUT:
        return back_in_and_out_func
    elif flag == INSTANT_IN:
        return instant_in_func
    elif flag == INSTANT_OUT:
        return instant_out_func
    else: # linear
        return linear
    
def scale_anchor_interpret(anchor: str, rect: pygame.Rect, pos: tuple[float, float], scale: tuple[float, float]) -> tuple[float, float]:
    """
    """
    added_surface_width = rect.width * (scale[0] - 1)
    added_surface_height = rect.height * (scale[1] - 1)

    if anchor == TOPLEFT:
        return (pos[0] + added_surface_width / 2, pos[1] + added_surface_height / 2) 

    elif anchor == TOPMID:
        return (pos[0], pos[1] + added_surface_height / 2)

    elif anchor == TOPRIGHT:
        return (pos[0] - added_surface_width / 2, pos[1] + added_surface_height / 2)

    elif anchor == MIDLEFT:
        return (pos[0] + added_surface_width / 2, pos[1])

    elif anchor == MIDRIGHT:
        return (pos[0] - added_surface_width / 2, pos[1])

    elif anchor == BOTTOMLEFT:
        return (pos[0] + added_surface_width / 2, pos[1] - added_surface_height / 2)

    elif anchor == BOTTOMMID:
        return (pos[0], pos[1] - added_surface_height / 2)

    elif anchor == BOTTOMRIGHT:
        return (pos[0] - added_surface_width / 2, pos[1] - added_surface_height / 2)

    elif anchor == CENTER:
        return pos
    
    else: # anchor == <offset coordinate value>
        return pos
    
def angle_anchor_interpret(anchor: str, rect: pygame.Rect, pos: tuple[float, float], scale: tuple[float, float], angle: float) -> tuple[float, float]:
    """
    """
    width = rect.width * scale[0]
    height = rect.height * scale[1]
    
    if anchor == TOPLEFT:
        x = width / 2; y = height / 2
    
    elif anchor == TOPMID:
        x = 0; y = height / 2

    elif anchor == TOPRIGHT:
        x = -width / 2; y = height / 2

    elif anchor == MIDLEFT:
        x = width / 2; y = 0

    elif anchor == MIDRIGHT:
        x = -width / 2; y = 0

    elif anchor == BOTTOMLEFT:
        x = width / 2; y = -height / 2

    elif anchor == BOTTOMMID:
        x = 0; y = -height / 2

    elif anchor == BOTTOMRIGHT:
        x = -width / 2; y = -height / 2

    elif anchor == CENTER:
        x = 0; y = 0

    else: # anchor == <offset coordinate value>
        x= 0; y = 0

    std_point = (
        pos[0] - x,
        pos[1] - y
    )

    return (
        std_point[0] + (x * cos(radians(-angle)) - y * sin(radians(-angle))),
        std_point[1] + (x * sin(radians(-angle)) + y * cos(radians(-angle)))
    )