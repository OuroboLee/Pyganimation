from pyganimation.core.interface.animation_interface import IAnimationBaseInterface
from pyganimation.core.interface.animation_script_interface import IAnimationScriptInterface
from pyganimation.elements import BaseAnimation, BaseVectorAnimation, Animation
from pyganimation._constants import *
from pyganimation.core.script_validation_check import *

import types

def list_to_default(script: list) -> dict:
    result_dict = dict()

    for animation in script:
        if not isinstance(animation, IAnimationBaseInterface):
            raise ValueError("Invalid animation list: the objects in list must be Animation / BaseAnimation / BaseVectorAnimation instance.")
        
        anim_dict = dict()

        if type(animation) in (BaseAnimation, BaseVectorAnimation):
            anim_dict[animation.animation_name] = {
                ANIMATION_SCRIPT: animation.get_animation_script(),
                ANIMATION_PARAM_INFO: {
                    START_FRAME: animation.start_frame,
                    END_FRAME: animation.end_frame,
                    SPEED: animation.speed,
                    LOOP: animation.loop,
                    IS_VISIBLE: animation.is_visible,
                    IS_REVERSED: animation.is_reversed,
                    ANIMATION_INFO: animation.animation_info
                }
            }

        elif type(animation) == Animation:
            pass

def dict_to_default(script: dict) -> dict:
    result_dict = dict()

    for name, info in script.items():
        result_dict[name] = dict()

        if ANIMATION_SCRIPT in info.keys(): # BaseAnimation / BaseVectorAnimation
            result_dict[name][ANIMATION_SCRIPT] = info[ANIMATION_SCRIPT]

            if ANIMATION_PARAM_INFO not in info.keys():
                result_dict[name][ANIMATION_PARAM_INFO] = ANIMATION_LIST_PARAM_INFO_DEFAULT.copy()

                if info[ANIMATION_SCRIPT].get_script_type() in (SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, SCRIPTTYPE_NORMAL_NORMAL_ANIMATION):
                    result_dict[name][ANIMATION_PARAM_INFO][ANIMATION_INFO] = NORMAL_ANIMATION_INFO_DEFAULT
                elif info[ANIMATION_SCRIPT].get_script_type() in (SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION, SCRIPTTYPE_NORMAL_VECTOR_ANIMATION):
                    result_dict[name][ANIMATION_PARAM_INFO][ANIMATION_INFO] = VECTOR_ANIMATION_INFO_DEFAULT

            else:
                result_dict[name][ANIMATION_PARAM_INFO] = _process_animation_param_info(
                    name, info[ANIMATION_PARAM_INFO], info[ANIMATION_SCRIPT]
                )

        elif ANIMATION_LIST in info.keys() and ANIMATION_TIMELINE in info.keys(): # Animation
            result_dict[name][ANIMATION_LIST] = info[ANIMATION_LIST]
            result_dict[name][ANIMATION_TIMELINE] = info[ANIMATION_LIST]

            if ANIMATION_PARAM_INFO not in info.keys():
                result_dict[name][ANIMATION_PARAM_INFO] = ANIMATION_LIST_PARAM_INFO_DEFAULT.copy()
                result_dict[name][ANIMATION_PARAM_INFO][ANIMATION_INFO] = NORMAL_ANIMATION_INFO_DEFAULT

            else:
                result_dict[name][ANIMATION_PARAM_INFO] = _process_animation_param_info(
                    name, info[ANIMATION_PARAM_INFO], info[ANIMATION_SCRIPT]
                )

        else:
            raise ValueError("Invaild dict-style animation_list: At least one AnimationScript / one AnimationList and one AnimationScript instance should be given.")
        
def _process_animation_param_info(name: str, param_info: dict, script: IAnimationScriptInterface) -> dict:
    result_param_info = dict()

    # Start Frame & End Frame
    if START_FRAME not in param_info.keys():
        result_param_info |= {
            START_FRAME: 1
        }
    else: 
        if not _frame_number_validation_check(param_info[START_FRAME]):
            raise ValueError(f"Start frame must be integer type between 1 and (animation_script's total_frame) - 1, or None in {name}.")

        result_param_info |= {
            START_FRAME: param_info[START_FRAME]
        }

    if END_FRAME not in param_info.keys():
        result_param_info |= {
             END_FRAME: None
        }  
    else:
        if not _frame_number_validation_check(param_info[END_FRAME]):
            raise ValueError(f"Start frame must be integer type between 1 and (animation_script's total_frame) - 1, or None in {name}.")

        result_param_info |= {
            END_FRAME: param_info[END_FRAME]
        }
                    
    if param_info[START_FRAME] == param_info[END_FRAME]:
        raise ValueError(f"Start frame must be different from End frame in {name}.")

    # Speed
    if SPEED not in param_info.keys():
        result_param_info |= {
            SPEED: 1
        }
    else:
        if not _speed_validation_check(param_info[SPEED]): 
            raise ValueError(f"Speed must be int | float larger than 0 in {name}.")
        
        result_param_info |= {
            SPEED: param_info[SPEED]
        }

    # Loop
    if LOOP not in param_info.keys():
        result_param_info |= {
            LOOP: 1
        }
    else:
        if not _loop_validation_check(param_info[LOOP]):
            raise ValueError(f"Loop must be int in {name}.")
        
        result_param_info |= {
            LOOP: param_info[LOOP]
        }

    # Is_visible

    if IS_VISIBLE not in param_info.keys():
        result_param_info |= {
            IS_VISIBLE: True
        }
    else:
        if not _boolean_validation_check(param_info[IS_VISIBLE]):
            raise ValueError(f"Is_visible must be bool in {name}.")
        
        result_param_info |= {
            IS_VISIBLE: param_info[IS_VISIBLE]
        }

    # Is_Reversed

    if IS_REVERSED not in param_info.keys():
        result_param_info |= {
            IS_REVERSED: True
        }
    else:
        if not _boolean_validation_check(param_info[IS_REVERSED]):
            raise ValueError(f"is_reversed must be bool in {name}.")
        
        result_param_info |= {
            IS_REVERSED: param_info[IS_REVERSED]
        }

    # Animation Info
    if ANIMATION_INFO not in param_info.keys():
        if script.get_script_type() in (SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, SCRIPTTYPE_NORMAL_NORMAL_ANIMATION):
            result_param_info |= {
                ANIMATION_INFO: NORMAL_ANIMATION_INFO_DEFAULT.copy()
            }
        elif script.get_script_type() in (SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION, SCRIPTTYPE_NORMAL_VECTOR_ANIMATION):
            result_param_info |= {
                ANIMATION_INFO: VECTOR_ANIMATION_INFO_DEFAULT.copy()
            }

    else:
        if script.get_script_type() in (SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION, SCRIPTTYPE_NORMAL_NORMAL_ANIMATION):
            if not _normal_animation_info_validation_check(param_info[ANIMATION_INFO]):
                raise ValueError(f"Invalid Animation Info in {name}.")
        
        elif script.get_script_type() in (SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION, SCRIPTTYPE_NORMAL_VECTOR_ANIMATION):
            if not _vector_animation_info_validation_check(param_info[ANIMATION_INFO]):
                raise ValueError(f"Invalid Animation Info in {name}.")

        result_param_info |= {
            ANIMATION_INFO: param_info[ANIMATION_INFO].copy()
        }

    return result_param_info

