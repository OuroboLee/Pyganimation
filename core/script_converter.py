# Purpose: Providing functions for converting 
# keyframe-normal / keyframe-vector dict style script to  
# normal-normal / normal-vector dict style script
# that is used in AnimationScript objects.
#
# Only for internal use.
#
#
#
#
#
#
#
#
#
#
#
#
# TODO: Making vector script converter
#

from pyganimation._constants import *
from itertools import pairwise

from pyganimation.core.math.interpolate_functions import get_func_from_interpolate_info
import pygame

from typing import Any



##############################################################

##### Main functions #####

def keyframe_normal_to_normal_normal(target_script: dict, debugging: bool = False) -> dict:
    """
    Converts keyframe_normal animation script to normal_normal animation script.

    ::param target_script:: Target keyframe script.
    ::param debugging:: 
    """

    result_script = dict()

    target_image = target_script[0][IMAGE_INFO][TARGET]

    image_info = {
        TARGET: target_image if type(target_image) == pygame.Surface else pygame.image.load(target_image),
        RECT: target_script[0][IMAGE_INFO][RECT]
    }
    
    result_script[0] = {
        IMAGE_INFO: image_info,
        POS: None,
        ANGLE: None,
        ANGLE_ANCHOR: None,
        SCALE: None,
        SCALE_ANCHOR: None,
        ALPHA: None
    }
    
    for key in list(result_script[0].keys()):
        if key not in (IMAGE_INFO, SCALE_ANCHOR, ANGLE_ANCHOR):
            result_script[0][key] = search_most_lately_presented_compo(
                target_script, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, key, 0
            )
    
    # POS

    image_info_normal_script = image_or_shape_info_keyframe_to_normal(
        convert_image_or_shape_info(IMAGE_INFO, target_script, debugging),
        IMAGE_INFO,
        debugging
    )

    pos_normal_script = component_keyframe_to_normal(
        convert_component(POS, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, target_script, debugging),
        POS, 
        debugging
    )

    # ANGLE

    angle_normal_script = component_keyframe_to_normal(
        convert_component(ANGLE, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, target_script, debugging), 
        ANGLE, 
        debugging
    )

    # SCALE

    scale_normal_script = component_keyframe_to_normal(
        convert_component(SCALE, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, target_script, debugging), 
        SCALE, 
        debugging
    )

    # ALPHA
    alpha_normal_script = component_keyframe_to_normal(
        convert_component(ALPHA, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, target_script, debugging),
        ALPHA, 
        debugging
    )

    # ANCHORING
    scale_anchor_normal_script = {}
    angle_anchor_normal_script = {}
    for i in range(0, list(target_script.keys())[-1] + 1):
        # SCALE ANCHOR
        current_scale_anchor = get_anchor(i, SCALE_ANCHOR, target_script, debugging)
        scale_anchor_normal_script[i] = current_scale_anchor

        if debugging:
            print(f"Current Scale Anchor in No.{i} frame : {current_scale_anchor}")

        # ANGLE ANCHOR
        current_angle_anchor = get_anchor(i, ANGLE_ANCHOR, target_script, debugging)
        angle_anchor_normal_script[i] = current_angle_anchor

        if debugging:
            print(f"Current Angle Anchor in No.{i} frame : {current_angle_anchor}")

    for i in range(1, list(target_script.keys())[-1] + 1):
        result_script |= {
            i : {IMAGE_INFO: image_info_normal_script[i][IMAGE_INFO],
                 POS: pos_normal_script[i][POS],
                 ANGLE: angle_normal_script[i][ANGLE],
                 ANGLE_ANCHOR: angle_anchor_normal_script[i],
                 SCALE: scale_normal_script[i][SCALE],
                 SCALE_ANCHOR: scale_anchor_normal_script[i],
                 ALPHA: alpha_normal_script[i][ALPHA]
            }
        }

    return result_script

def keyframe_vector_to_normal_vector(target_script: dict, debugging: bool = False) -> dict:
    pass


##### Assistant Functions #####

def get_anchor(current_frame_num: int, 
               target_anchor: str, 
               target_script: dict, 
               debugging: bool = False) -> str:
    
    if current_frame_num == 0:
        return get_anchor(1, target_anchor, target_script, debugging)

    keyframe_numbers = list(target_script.keys())
    target_keyframe_number = find_most_close_keyframe_after_frame_number(current_frame_num, keyframe_numbers)

    if target_keyframe_number == keyframe_numbers[-1]:
        if KEYFRAME_INTERPOLATE_INFO in target_script[target_keyframe_number].keys():
            if target_anchor in target_script[target_keyframe_number][KEYFRAME_INTERPOLATE_INFO]:
                return target_script[target_keyframe_number][KEYFRAME_INTERPOLATE_INFO][target_anchor]

            else: return CENTER
        else: return CENTER
    else:
        if KEYFRAME_INTERPOLATE_INFO in target_script[target_keyframe_number].keys():
            if target_anchor in target_script[target_keyframe_number][KEYFRAME_INTERPOLATE_INFO]:
                return target_script[target_keyframe_number][KEYFRAME_INTERPOLATE_INFO][target_anchor]
                    
            else:
                return get_anchor(target_keyframe_number + 1, target_anchor, target_script, debugging)
        else: return get_anchor(target_keyframe_number+ 1, target_anchor, target_script, debugging)

def get_info(current_frame_num: int, 
             target_info: str, 
             target_script: dict,
             debugging: bool = False) -> dict:

    keyframe_numbers = list(target_script.keys())
    target_keyframe_number = find_most_close_keyframe_before_frame_number(current_frame_num, keyframe_numbers)

    if target_info in target_script[target_keyframe_number].keys():
        return target_script[target_keyframe_number][target_info]
    
    else:
        if target_keyframe_number == 0:
            return target_script[target_keyframe_number][target_info]
        else:
            return get_info(target_keyframe_number - 1, target_info, target_script, debugging)
            
def find_most_close_keyframe_after_frame_number(frame_num: int, target_keyframe_list: list[int]):
    for keyframe_number in target_keyframe_list[1:]:
        if keyframe_number >= frame_num: return keyframe_number

def find_most_close_keyframe_before_frame_number(frame_num: int,
                                                 target_keyframe_list: list[int]):
    for keyframe_number in target_keyframe_list[::-1]:
        if keyframe_number <= frame_num: return keyframe_number

def image_or_shape_info_keyframe_to_normal(target_info_dict: dict, 
                                           target_info: str, 
                                           debugging: bool = False) -> dict:
    result_dict = dict()

    keyframe_number_pair = list(pairwise(target_info_dict.keys()))

    for pair in keyframe_number_pair:
        for i in range(pair[0], pair[1] + 1):
            target = target_info_dict[pair[0]][target_info][TARGET]
            if target_info == IMAGE_INFO:
                result_dict[i] = {
                    target_info: {
                        TARGET: target if type(target) == pygame.Surface else pygame.image.load(target),
                        RECT: target_info_dict[pair[0]][target_info][RECT]
                    }   
                }

            elif target_info == SHAPE_INFO:
                result_dict[i] = {
                    target_info: {
                        TARGET: target,
                        INFO: target_info_dict[pair[0]][target_info][INFO]
                    }
                }

    return result_dict

def component_keyframe_to_normal(target_compo_dict: dict, 
                                 target_compo: str, 
                                 debugging: bool = False) -> dict:

    result_dict = {
        0: {
            target_compo: target_compo_dict[0][KEYFRAME_NORMAL_INFO]
        }
    }

    keyframe_number_pair = list(pairwise(target_compo_dict.keys()))

    for pair in keyframe_number_pair:
        result_dict |= component_interpolate(target_compo, 
                                             target_compo_dict[pair[0]], target_compo_dict[pair[1]],
                                             pair[0], pair[1], debugging)

    return result_dict

    

def component_interpolate(target_compo: str, start_frame_info: dict, end_frame_info: dict, start_frame_num: int, end_frame_num: int, debugging: bool):
    start = start_frame_info[KEYFRAME_NORMAL_INFO]
    end = end_frame_info[KEYFRAME_NORMAL_INFO]
    interpolate_info = end_frame_info[KEYFRAME_INTERPOLATE_INFO]

    total_frame_num = end_frame_num - start_frame_num

    result_dict = dict()
    
    if target_compo in (POS, SCALE):
        dx = (end[0] - start[0]) / total_frame_num
        dy = (end[1] - start[1]) / total_frame_num

        accumulated_duo = start

        if type(interpolate_info) == str:
            x_interpolate_function = get_func_from_interpolate_info(interpolate_info)
            y_interpolate_function = get_func_from_interpolate_info(interpolate_info)

        else: # duo : list / tuple
            x_interpolate_function = get_func_from_interpolate_info(interpolate_info[0])
            y_interpolate_function = get_func_from_interpolate_info(interpolate_info[1])

        for i in range(1, total_frame_num):
            accumulated_duo = (
                accumulated_duo[0] + 0.5 * dx * (x_interpolate_function(total_frame_num, i-1) + x_interpolate_function(total_frame_num, i)),
                accumulated_duo[1] + 0.5 * dy * (y_interpolate_function(total_frame_num, i-1) + y_interpolate_function(total_frame_num, i)),
            )

            result_dict |= {
                start_frame_num + i: {
                    target_compo: accumulated_duo
                }
            }
    
    elif target_compo == COLOR:
        dr = (end[0] - start[0]) / total_frame_num
        dg = (end[1] - start[1]) / total_frame_num
        db = (end[2] - start[2]) / total_frame_num

        accumulated_trio = start

        if type(interpolate_info) == str: 
            r_interpolate_function = get_func_from_interpolate_info(interpolate_info)
            g_interpolate_function = get_func_from_interpolate_info(interpolate_info)
            b_interpolate_function = get_func_from_interpolate_info(interpolate_info)
        else: # trio : list / tuple
            r_interpolate_function = get_func_from_interpolate_info(interpolate_info[0])
            g_interpolate_function = get_func_from_interpolate_info(interpolate_info[1])
            b_interpolate_function = get_func_from_interpolate_info(interpolate_info[2])

        for i in range(i, total_frame_num):
            accumulated_trio = (
                accumulated_trio[0] + 0.5 * dr * (r_interpolate_function(total_frame_num, i-1) + r_interpolate_function(total_frame_num, i)),
                accumulated_trio[1] + 0.5 * dg * (g_interpolate_function(total_frame_num, i-1) + g_interpolate_function(total_frame_num, i)),
                accumulated_trio[2] + 0.5 * db * (b_interpolate_function(total_frame_num, i-1) + b_interpolate_function(total_frame_num, i)),
            )

            result_dict |= {
                start_frame_num + i: {
                    target_compo: accumulated_trio
                }
            }

    else:
        delta = (end - start) / total_frame_num

        accumulated = start

        interpolate_function = get_func_from_interpolate_info(interpolate_info)

        for i in range(1, total_frame_num):
            accumulated += 0.5 * delta * (interpolate_function(total_frame_num, i-1) + interpolate_function(total_frame_num, i))

            result_dict |= {
                start_frame_num + i: {
                    target_compo: accumulated
                }
            }
        
    
    result_dict |= {
        end_frame_num: {
            target_compo: end_frame_info[KEYFRAME_NORMAL_INFO]
        }
    }

    return result_dict

def convert_image_or_shape_info(target_info: str,
                                target_script: dict,
                                debugging: bool = False) -> dict:
    """
    :param target_info: Target script info. IMAGE_INFO / SHAPE_INFO
    :param target_script: Target keyframe script.
    :param debugging:
    """
    result_dict = dict()

    for frame_num, frame in target_script.items():
        new_frame = dict()

        if target_info in frame.keys():
            new_frame[target_info] = frame[target_info]
        else:
            new_frame[target_info] = get_info(frame_num, 
                                              target_info, 
                                              target_script, 
                                              debugging)
        
        result_dict |= {frame_num: new_frame}

    return result_dict



def convert_component(target_compo: str, 
                      script_type: str, 
                      target_script: dict, 
                      debugging: bool = False) -> dict:
    """
    :param target_compo: Target script component. Ex) POS, ANGLE, . . . 
    :param script_type: Script Type. SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION or SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION
    :param target_script: Target keyframe script.
    :param debugging:
    """

    result_dict = dict()

    last_frame_num = list(target_script.keys())[-1]

    for frame_num, frame in target_script.items():
        new_frame = dict()
        is_target_compo_in_current_frame_normal_info = KEYFRAME_NORMAL_INFO in frame.keys() and target_compo in frame[KEYFRAME_NORMAL_INFO].keys()
        is_target_compo_in_current_frame_interpolate_info = KEYFRAME_INTERPOLATE_INFO in frame.keys() and target_compo in frame[KEYFRAME_INTERPOLATE_INFO].keys()



        if frame_num != 0:
            if is_target_compo_in_current_frame_interpolate_info:
                new_frame |= {
                    KEYFRAME_INTERPOLATE_INFO: frame[KEYFRAME_INTERPOLATE_INFO][target_compo]
                }
            else:
                new_frame |= {
                    KEYFRAME_INTERPOLATE_INFO: LINEAR
                }
        
        if frame_num in (0, last_frame_num):
            if is_target_compo_in_current_frame_normal_info:
                new_frame |= {
                    KEYFRAME_NORMAL_INFO: frame[KEYFRAME_NORMAL_INFO][target_compo]
                }

            else: 
                new_frame |= {
                    KEYFRAME_NORMAL_INFO: search_most_lately_presented_compo(
                        target_script, script_type, target_compo, frame_num
                    )
                }
        else:
            if is_target_compo_in_current_frame_normal_info:
                new_frame |= {
                    KEYFRAME_NORMAL_INFO: frame[KEYFRAME_NORMAL_INFO][target_compo]
                }

        if frame_num in (0, last_frame_num) or is_target_compo_in_current_frame_normal_info:
            result_dict |= {frame_num: new_frame}

    if debugging:
        print(f"{target_compo} : {result_dict}")
                  
    return result_dict
    
def search_most_lately_presented_compo(target_script: dict, script_type: str, target_compo: str, frame_num: int) -> Any:
    if frame_num == 0:
        if KEYFRAME_NORMAL_INFO in target_script[frame_num].keys() and target_compo in target_script[frame_num][KEYFRAME_NORMAL_INFO]:
            return target_script[frame_num][KEYFRAME_NORMAL_INFO][target_compo]
        else:
            if script_type == SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION:
                return KEYFRAME_NORMAL_ZERO_FRAME_DEFAULT[target_compo]
            
            elif script_type == SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION:
                return KEYFRAME_VECTOR_ZERO_FRAME_DEFAULT[target_compo]
        
    else:
        if KEYFRAME_NORMAL_INFO in target_script[frame_num].keys() and target_compo in target_script[frame_num][KEYFRAME_NORMAL_INFO].keys():
            return target_script[frame_num][KEYFRAME_NORMAL_INFO][target_compo]
            
        else:
            frame_num_list = list(target_script.keys())
            return search_most_lately_presented_compo(
                target_script, script_type, target_compo, 
                frame_num_list[frame_num_list.index(frame_num) - 1]
            ) 

if __name__ == "__main__" :
    keyframe_script = {
        0: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((50, 50)),
                RECT: 0
            }
        },
        1: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((50, 50)),
                RECT: 0
            }
        },
        20: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((40, 40)),
                RECT: 0
            }
            
        },
        40: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((30, 30)),
                RECT: 0
            }
        },
        60: {
            IMAGE_INFO: {
                TARGET: pygame.Surface((30, 30)),
                RECT: 0
            }
        }
    }

    print(keyframe_normal_to_normal_normal(keyframe_script, True))