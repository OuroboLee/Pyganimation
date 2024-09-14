# Purpose: Providing functions for converting 
# keyframe-normal / keyframe-vector dict style script to  
# normal-normal / normal-vector dict style script
# that is used in AnimationScript objects.
#
# Converting Process:
# 
# Example Keyframe Script:
# {
#     0: {
#         IMAGE_INFO: {
#             TARGET: example_image,
#             RECT: None
#         },
#         KEYFRAME_NORMAL_INFO: {
#             POS: (400, 200)
#         }
#     },
#     1: {
#         KEYFRAME_NORMAL_INFO: {
#             POS: (400, 200)
#         }
#     },
#     60: {
#         KEYFRAME_NORMAL_INFO: {
#             POS: (600, 400)
#         },
#         KEYFRAME_INTERPOLATE_INFO: {
#             POS: SIN_IN_AND_OUT
#         }
#     },
#     120: {
#         KEYFRAME_NORMAL_INFO: {
#             POS: (800, 200)
#         },
#         KEYFRAME_INTERPOLATE_INFO: {
#             POS: BACK_IN_AND_OUT
#         }
#     },
#     180: {
#         KEYFRAME_NORMAL_INFO: {
#             POS: (400, 200)
#         },
#         KEYFRAME_INTERPOLATE_INFO: {
#             POS: EXPO_IN
#         }
#     }
# }
#                   |
#                   V
# 1. Seperate each components. (Example is only for POS.)
# If there is a value not given, converter will autometically guess the value.
# {
#     0: {
#         KEYFRAME_NORMAL_INFO: (400, 200)
#     },
#     1: {
#         KEYFRAME_NORMAL_INFO: (400, 200),
#         KEYFRAME_INTERPOLATE_INFO: LINEAR
#     },
#     60: {
#         KEYFRAME_NORMAL_INFO: (600, 400),
#         KEYFRAME_INTERPOLATE_INFO: SIN_IN_AND_OUT
#     },
#     120: {
#         KEYFRAME_NORMAL_INFO: (800, 200),
#         KEYFRAME_INTERPOLATE_INFO: BACK_IN_AND_OUT
#     },
#     180: {
#         KEYFRAME_NORMAL_INFO: (400, 200),
#         KEYFRAME_INTERPOLATE_INFO: EXPO_IN
#     }
# }
#                   |
#                   V
# 2. Perform interpolation work for each component's dict.
# (Example will be added.)
#
# 3. Combine each component's dict into normal-style dict.
# (Example will be added.)
#
#
#
#
#
#
#
# Only for internal use.
#
# TODO: Making vector script converter
#

from pyganimation._constants import *
from itertools import pairwise

from pyganimation.core.math.interpolate_functions import get_func_from_interpolate_info, scale_anchor_interpret, angle_anchor_interpret
from pyganimation.core.math.followable_shape import BezierCurve
from pyganimation.core.math.tools import is_negative
from pyganimation.core.validation_check import *

import pygame

from typing import Any



##############################################################

##### Core Functions #####

def keyframe_normal_to_final_script(target_script: dict, debugging: bool = False) -> dict:
    return normal_normal_to_final_script(
        keyframe_normal_to_normal_normal(target_script, debugging), debugging
    )

def keyframe_vector_to_final_script(target_script: dict, debugging: bool = False) -> dict:
    return normal_vector_to_final_script(
        keyframe_vector_to_normal_vector(target_script, debugging), debugging
    )

__all__ = ["keyframe_normal_to_final_script",
           "keyframe_normal_to_final_script",
           "normal_normal_to_final_script",
           "normal_vector_to_final_script"]

##### Segment functions #####

def keyframe_normal_to_normal_normal(target_script: dict, debugging: bool = False) -> dict:
    """
    Converts keyframe_normal animation script to normal_normal animation script.

    ::param target_script:: Target keyframe script.
    ::param debugging:: If print debugging information in conversion process at stdout or not.
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
    
    

    image_info_normal_script = image_or_shape_info_keyframe_to_normal(
        convert_image_or_shape_info(IMAGE_INFO, target_script, debugging),
        IMAGE_INFO,
        debugging
    )
    
    # POS

    pos_normal_script = component_keyframe_to_normal(
        convert_component(POS, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, target_script, debugging),
        POS, 
        debugging
    )
    print(convert_component(POS, SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, target_script, debugging))

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

def normal_normal_to_final_script(target_script: dict, debugging: bool = False) -> tuple[list[pygame.Surface], dict]:
    total_frame = list(target_script.keys())[-1] + 1

    surfaces = list()
    info = list()

    for i in range(total_frame):
        current_image = target_script[i][IMAGE_INFO][TARGET]
        current_image_rect = target_script[i][IMAGE_INFO][RECT]

        current_pos = target_script[i][POS]
        current_angle = target_script[i][ANGLE]
        current_scale = (
            abs(target_script[i][SCALE][0]), abs(target_script[i][SCALE][1])                   
        )
        current_filp = (
            is_negative(target_script[i][SCALE][0]), is_negative(target_script[i][SCALE][1])
        )
        current_alpha = target_script[i][ALPHA]

        if current_alpha > 255: current_alpha = 255
        elif current_alpha < 0: current_alpha = 0

        manipulated_image = pygame.transform.chop(current_image, current_image_rect)
        manipulated_image = pygame.transform.scale_by(manipulated_image, current_scale)
        manipulated_image = pygame.transform.rotate(manipulated_image, current_angle)
        manipulated_image.set_alpha(current_alpha)

        # ANCHORING
        current_scale_anchor = target_script[i][SCALE_ANCHOR]
        current_pos = scale_anchor_interpret(
            current_scale_anchor, current_image.get_rect(),
            current_pos, current_scale
        )

        current_angle_anchor = target_script[i][ANGLE_ANCHOR]
        current_pos = angle_anchor_interpret(
            current_angle_anchor, current_image.get_rect(),
            current_pos, current_scale, current_angle
        )

        surfaces.append(manipulated_image)

        info.append(
            {
                POS: current_pos,
                FLIP: current_filp
            }
        )

    return surfaces, info

def normal_vector_to_final_script(target_script: dict, debugging: bool = False) -> tuple[list[pygame.Surface], dict]:
    pass

##### Search Relative Functions #####
    
def search_most_lately_presented_compo(target_script: dict, 
                                       script_type: str, 
                                       target_compo: str, 
                                       frame_num: int,
                                       debugging: bool = False) -> Any:
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
                frame_num_list[frame_num_list.index(frame_num) - 1])

        

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
            
def find_most_close_keyframe_after_frame_number(frame_num: int, 
                                                target_keyframe_list: list[int]):
    for keyframe_number in target_keyframe_list[1:]:
        if keyframe_number >= frame_num: return keyframe_number

def find_most_close_keyframe_before_frame_number(frame_num: int,
                                                 target_keyframe_list: list[int]):
    for keyframe_number in target_keyframe_list[::-1]:
        if keyframe_number <= frame_num: return keyframe_number

##### Component Keyframe -> Normal Functions #####

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

    if debugging:
        print(f"==================== Starting Component Interpolation Process : {target_compo} ====================")

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

def component_interpolate(target_compo: str, 
                          start_frame_info: dict, end_frame_info: dict, 
                          start_frame_num: int, end_frame_num: int, 
                          debugging: bool):
    if debugging:
        print(f"-------------------- Starting Component Interpolation Process : {target_compo}, {start_frame_num}~{end_frame_num} --------------------")
        print(f"Start Frame Info: {start_frame_info}")
        print(f"End Frame Info: {end_frame_info}")
        print()

    start = start_frame_info[KEYFRAME_NORMAL_INFO]
    end = end_frame_info[KEYFRAME_NORMAL_INFO]
    interpolate_info = end_frame_info[KEYFRAME_INTERPOLATE_INFO]
    special_info = end_frame_info[KEYFRAME_SPECIAL_INFO]
    curve_info = end_frame_info[CURVE]

    total_frame_num = end_frame_num - start_frame_num

    if debugging:
        print(f"Start Value: {start}")
        print(f"End Value: {end}")
        print(f"Interpolation Function: {interpolate_info}")
        print(f"Special Information: {special_info}")
        print(f"Curve Information: {curve_info}")
        print()

    result_dict = dict()
    
    if target_compo in (POS, SCALE):
        if target_compo == POS and special_info is not None:
            if special_info == FOLLOW_CURVE:
                if type(interpolate_info) != str:
                    pass

                interpolate_function = get_func_from_interpolate_info(interpolate_info)
                
                dt = 1 / total_frame_num
                accumulated_t = 0

                if debugging:
                    print(f"Delta - t : {dt}")
                    print(f"Current Accumulated Sum: {accumulated_t}")
                    print()


                for i in range(1, total_frame_num):
                    accumulated_t += 0.5 * dt * (interpolate_function(total_frame_num, i-1) + interpolate_function(total_frame_num, i))

                    result_dict |= {
                        start_frame_num + i: {
                            target_compo: curve_info.get_pos(accumulated_t)
                        }
                    }

                    if debugging:
                        print(f"Current Working Frame: {start_frame_num + i}")
                        print(f"Current Accumulated Sum: {accumulated_t}")
                        print(f"Current Frame {target_compo}: {curve_info.get_pos(accumulated_t)}")
                        print()

        
        else:
            dx = (end[0] - start[0]) / total_frame_num
            dy = (end[1] - start[1]) / total_frame_num

            accumulated_duo = start

            if debugging:
                    print(f"Delta - x : {dx}")
                    print(f"Delta - y : {dy}")
                    print(f"Current Accumulated Sum: {accumulated_t}")
                    print()

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

                if debugging:
                    print(f"Current Working Frame: {start_frame_num + i}")
                    print(f"Current Accumulated Sum: {accumulated_duo}")
                    print(f"Current Frame {target_compo}: {accumulated_duo}")
                    print()

    
    elif target_compo == COLOR:
        dr = (end[0] - start[0]) / total_frame_num
        dg = (end[1] - start[1]) / total_frame_num
        db = (end[2] - start[2]) / total_frame_num

        accumulated_trio = start

        if debugging:
            print(f"Delta - red : {dr}")
            print(f"Delta - green : {dg}")
            print(f"Delta - blue : {db}")
            print(f"Current Accumulated Sum: {accumulated_trio}")
            print()

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
            if debugging:
                print(f"Current Working Frame: {start_frame_num + i}")
                print(f"Current Accumulated Sum: {accumulated_trio}")
                print(f"Current Frame {target_compo}: {accumulated_trio}")
                print()

    else:
        if target_compo == ANGLE and special_info is not None:
            if special_info == FOLLOW_CURVE:
                if type(interpolate_info) != str:
                    pass

                interpolate_function = get_func_from_interpolate_info(interpolate_info)
                
                dt = 1 / total_frame_num
                accumulated_t = 0

                if debugging:
                    print(f"Delta - t : {dt}")
                    print(f"Current Accumulated Sum: {accumulated_t}")
                    print()

                for i in range(1, total_frame_num):
                    accumulated_t += 0.5 * dt * (interpolate_function(total_frame_num, i-1) + interpolate_function(total_frame_num, i))

                    result_dict |= {
                        start_frame_num + i: {
                            target_compo: curve_info.get_angle(accumulated_t)
                        }
                    }
                    if debugging:
                        print(f"Current Working Frame: {start_frame_num + i}")
                        print(f"Current Accumulated Sum: {accumulated_t}")
                        print(f"Current Frame {target_compo}: {curve_info.get_angle(accumulated_t)}")
                        print()

        else:
            delta = (end - start) / total_frame_num
            accumulated = start

            if debugging:
                print(f"Delta : {delta}")
                print(f"Current Accumulated Sum: {accumulated_t}")
                print()

            interpolate_function = get_func_from_interpolate_info(interpolate_info)

            for i in range(1, total_frame_num):
                accumulated += 0.5 * delta * (interpolate_function(total_frame_num, i-1) + interpolate_function(total_frame_num, i))

                result_dict |= {
                    start_frame_num + i: {
                        target_compo: accumulated
                    }
                }
                if debugging:
                    print(f"Current Working Frame: {start_frame_num + i}")
                    print(f"Current Accumulated Sum: {accumulated}")
                    print(f"Current Frame {target_compo}: {accumulated}")
                    print()
        
    
    result_dict |= {
        end_frame_num: {
            target_compo: end_frame_info[KEYFRAME_NORMAL_INFO]
        }
    }

    return result_dict

##### Script Seperation #####

def convert_image_or_shape_info(target_info: str,
                                target_script: dict,
                                debugging: bool = False) -> dict:
    """
    Seperates Image / Shape info from target script.

    :param target_info: Target script info. IMAGE_INFO / SHAPE_INFO
    :param target_script: Target keyframe script.
    :param debugging:
    """
    if debugging:
        print()

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
            
        if debugging:
            pass

        if target_info == IMAGE_INFO:
            _image_info_validation_check(new_frame[target_info])
        elif target_info == SHAPE_INFO:
            _shape_info_validation_check(new_frame[target_info])

        
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

    if debugging:
        print(f"-------------------- Starting Component Conversion Process : {target_compo} --------------------")

    result_dict = dict()

    last_frame_num = list(target_script.keys())[-1]

    for frame_num, frame in target_script.items():
        new_frame = dict()
        
        
        is_target_compo_in_current_frame_normal_info = _is_target_in_current_frame(
            target_compo, KEYFRAME_NORMAL_INFO, frame, frame_num
        )
        is_target_compo_in_current_frame_interpolate_info = _is_target_in_current_frame(
            target_compo, KEYFRAME_INTERPOLATE_INFO, frame, frame_num
        )
        is_target_compo_in_current_frame_special_info = _is_target_in_current_frame(
            target_compo, KEYFRAME_SPECIAL_INFO, frame, frame_num
        )
        is_curve_in_current_frame_special_info = _is_target_in_current_frame(
            CURVE, KEYFRAME_SPECIAL_INFO, frame, frame_num
        )

        # Interpolate Info
        if frame_num != 0:
            if is_target_compo_in_current_frame_interpolate_info:
                new_frame |= {
                    KEYFRAME_INTERPOLATE_INFO: frame[KEYFRAME_INTERPOLATE_INFO][target_compo]
                }
            else:
                new_frame |= {
                    KEYFRAME_INTERPOLATE_INFO: LINEAR
                }

            if new_frame[KEYFRAME_INTERPOLATE_INFO] not in INTERPOLATE_FUNC_LIST:
                raise ValueError(f"Wrong Script: Invalid Interpolation Function in No.{frame_num} Keyframe.")

        
            # Special Info (For only POS, ANGLE now.)
            if is_target_compo_in_current_frame_special_info:
                new_frame |= {
                    KEYFRAME_SPECIAL_INFO: frame[KEYFRAME_SPECIAL_INFO][target_compo]
                }
            else:
                new_frame |= {
                    KEYFRAME_SPECIAL_INFO: None
                }

            if new_frame[KEYFRAME_SPECIAL_INFO] not in SPECIAL_LIST:
                raise ValueError(f"Wrong Script: Invalid Special Operation Info in No.{frame_num} Keyframe.")

            if is_curve_in_current_frame_special_info:
                curve = frame[KEYFRAME_SPECIAL_INFO][CURVE]
                if type(curve) in (BezierCurve, ):
                    new_frame |= {
                        CURVE: frame[KEYFRAME_SPECIAL_INFO][CURVE]
                    }

                elif type(curve) in (list, tuple):
                    if type(curve[0]) != str:
                        raise ValueError(f"Wrong Script: If type of curve is list or tuple, the object in the first index should be str representing supported followable shapes, like 'bezier', in No.{frame_num} Keyframe.")

                    if curve[0] == BEZIER:
                        new_frame |= {
                            CURVE: BezierCurve(curve[1])
                        }
                    
                    elif curve[0] == ARC:
                        pass

                    else:
                        raise ValueError(f"Wrong Script: If type of curve is list or tuple, the object in the first index should be str representing supported followable shapes, like 'bezier', in No.{frame_num} Keyframe.")
                
                else:
                    raise ValueError(f"Wrong Script: The type of curve should be FollowableShape, list or tuple.")

            else: 
                new_frame |= {
                    CURVE: None
                }

            if new_frame[KEYFRAME_SPECIAL_INFO] == None and new_frame[CURVE] != None:
                raise ValueError(f"Wrong Script: There is no special info while curve is given in No.{frame_num} Keyframe.")
            
        
        # Normal Info
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

            if not is_target_compo_in_current_frame_normal_info and is_target_compo_in_current_frame_interpolate_info:
                raise ValueError(f"Wrong Script: Detected Interpolate Info in frame that does not have Normal Info in No.{frame_num} Keyframe.")

        if frame_num in (0, last_frame_num) or is_target_compo_in_current_frame_normal_info:
            result_dict |= {frame_num: new_frame}

    if debugging:
        print(f"{target_compo} : {result_dict}")
                  
    return result_dict

def _is_target_in_current_frame(target: str, target_keyframe_info: str, frame: dict, frame_num: int) -> bool:
    if target_keyframe_info not in frame.keys():
        return False
    else:
        if target not in frame[target_keyframe_info].keys():
            return False
        else:
            return True


            

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