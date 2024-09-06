from pyganimation._constants import *
from pyganimation.animation_manager import AnimationManager
from pyganimation.elements import *

__all__ = [
    ##### Constants #####
    
    # Script Type
    "SCRIPTTYPE_NORMAL_NORMAL_ANIMATION",
    "SCRIPTTYPE_NORMAL_VECTOR_ANIMATION",
    "SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION",
    "SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION",

    # For Writing Animation Script
    "IMAGE_INFO",
    "SHAPE_INFO",
    "TARGET",
    "RECT",
    "INFO",

    "POS",
    "ANGLE",
    "SCALE",
    "ALPHA",
    "COLOR",
    "COLORKEY",

    "ABS_POS",
    "ABS_ANGLE",
    "ABS_SCALE",
    "ABS_ALPHA",
    "ABS_COLOR",

    "NORMAL_ANIMATION_INFO_DEFAULT",

    "INF",

    # Animation List

    # Animation Timeline

    # Shape / Vector

    # Interpolate Function
    "SCALE_ANCHOR",
    "ANGLE_ANCHOR",

    "LINEAR",
    "SIN_IN",
    "SIN_OUT",
    "SIN_IN_AND_OUT",
    "BACK_IN",
    "BACK_OUT",
    "BACK_IN_AND_OUT",
    "EXPO_IN",
    "EXPO_OUT",
    "INSTANT_IN",
    "INSTANT_OUT",

    # Keyframe
    "KEYFRAME_NORMAL_INFO",
    "KEYFRAME_INTERPOLATE_INFO",

    # Scale Anchor 
    "TOPLEFT",
    "TOPMID",
    "TOPRIGHT",
    "MIDLEFT",
    "CENTER",
    "MIDRIGHT",
    "BOTTOMLEFT",
    "BOTTOMMID",
    "BOTTOMRIGHT"

    ##### Elements #####

    "BaseAnimation",
    "BaseVetorAnimation",
    "AnimationScript",
    "SpriteAnimationScript",
    "AnimationList",

    ##### AnimaitonManager #####

    "AnimationManager"
]

__version__ = "0.1.0"