# Script Type

SCRIPTTYPE_NORMAL_NORMAL_ANIMATION = "normal_normal"
SCRIPTTYPE_NORMAL_VECTOR_ANIMATION = "normal_vector"
SCRIPTTYPE_KEYFRAME_NORMAL_ANIMATION = "keyframe_normal"
SCRIPTTYPE_KEYFRAME_VECTOR_ANIMATION = "keyframe_vector"

# Animation Script

JSON = ".json"

IMAGE_INFO = "image_information"
SHAPE_INFO = "shape_information"
TARGET = "target"
RECT = "rect"
INFO = "info"

POS = "pos"
ANGLE = "angle"
SCALE = "scale"
ALPHA = "alpha"
COLOR = "color"
COLORKEY = "colorkey"

ABS_POS = "abs_pos"
ABS_ANGLE = "abs_angle"
ABS_SCALE = "abs_scale"
ABS_ALPHA = "abs_alpha"
ABS_COLOR = "abs_color"

NORMAL_ANIMATION_INFO_DEFAULT = {
    ABS_POS: (0, 0),
    ABS_ANGLE: 0,
    ABS_SCALE: (1, 1),
    ABS_ALPHA: 1,
    COLORKEY: None
}

VECTOR_ANIMATION_INFO_DEFAULT = {

}

INF = "infinity"


##### ANIMATION LIST #####

ANIMATION_TYPE = "animation_type"
ANIMATION_SCRIPT = "animation_script"
ANIMATION_LIST = "animation_list"
ANIMATION_TIMELINE = "animation_timeline"
ANIMATION_PARAM_INFO = "animation_param_info"

START_FRAME = "start_frame"
END_FRAME = "end_frame"
SPEED = "speed"
LOOP = "loop"
IS_VISIBLE = "is_visible"
IS_REVERSED = "is_reversed"
ANIMATION_INFO = "animation_info"

ANIMATION_LIST_PARAM_INFO_DEFAULT = {
    START_FRAME: 1,
    END_FRAME: None,
    SPEED: 1,
    LOOP: 1,
    IS_VISIBLE: True,
    IS_REVERSED: False
}

# Shape / Vector

ELLIPSE = "ellipse"
RECTANGLE = "rectangle"
SQUARE = "square"
CIRCLE = "circle"
ARC = "arc"
PIE = "pie"
LINE = "line"
LINES = "lines"
BEZIER = "bezier"


SHAPE_LIST = [
    ELLIPSE, 
    RECTANGLE, 
    SQUARE, 
    CIRCLE, 
    ARC, 
    PIE, 
    LINE, 
    LINES,
    BEZIER
]

BORDER_WIDTH = "border_width"
RADIUS = "radius"
LENGTH = "length"
START_ANGLE = "start_angle"
END_ANGLE = "end_angle"
INTERVAL_ANGLE = "interval_angle"
START_POS = "start_pos"
END_POS = "end_pos"

POS_LIST = "pos_list"

BORDER_RADIUS = "border_radius"
TOPLEFT_BORDER_RADIUS = "topleft_border_radius"
TOPRIGHT_BORDER_RADIUS = "topright_border_radius"
BOTTOMLEFT_BORDER_RADIUS = "bottomleft_border_radius"
BOTTOMRIGHT_BORDER_RADIUS = "bottomright_border_radius"

# Interpolate Function

FOLLOW_CURVE = "follow_curve"
CURVE = "curve"

SPECIAL_LIST = [
    FOLLOW_CURVE,
    None
]

POS_ANCHOR = "pos_anchor"
SCALE_ANCHOR = "scale_anchor"
ANGLE_ANCHOR = "angle_anchor"

LINEAR = "linear"
SIN_IN = "sin_in"
SIN_OUT = "sin_out"
SIN_IN_AND_OUT = "sin_in_and_out"
BACK_IN = "back_in"
BACK_OUT = "back_out"
BACK_IN_AND_OUT = "back_in_and_out"
EXPO_IN = "expo_in"
EXPO_OUT = "expo_out"
EXPO_IN_AND_OUT = "expo_in_and_out"
BOUNCE_IN = "bounce_in"
BOUNCE_OUT = "bounce_out"
BOUNCE_IN_AND_OUT = "bounce_in_and_out"
INSTANT_IN = "instant_in"
INSTANT_OUT = "instant_out"

INTERPOLATE_FUNC_LIST = [
    LINEAR,
    SIN_IN,
    SIN_OUT,
    SIN_IN_AND_OUT,
    BACK_IN,
    BACK_IN_AND_OUT,
    BACK_OUT,
    EXPO_IN,
    EXPO_IN_AND_OUT,
    EXPO_OUT,
    INSTANT_IN,
    INSTANT_OUT
]

# Keyframe

KEYFRAME_NORMAL_INFO = "keyframe_normal_info"
KEYFRAME_INTERPOLATE_INFO = "keyframe_interpolate_info"
KEYFRAME_SPECIAL_INFO = "keyframe_special_info"

# Scale Anchor & Rect

TOPLEFT = "topleft"
TOPMID = "topmid"
TOPRIGHT = "topright"
MIDLEFT = "midleft"
CENTER = "center"
MIDRIGHT = "midright"
BOTTOMLEFT = "bottomleft"
BOTTOMMID = "bottommid"
BOTTOMRIGHT = "bottomright"

ANCHOR_LIST = [
    TOPLEFT,
    TOPMID,
    TOPRIGHT,
    MIDLEFT,
    CENTER,
    MIDRIGHT,
    BOTTOMLEFT,
    BOTTOMMID,
    BOTTOMRIGHT
]

TOP = "top"
LEFT = "left"
MID = "mid"
RIGHT = "right"
BOTTOM = "bottom"
WIDTH = "width"
HEIGHT = "height"
HALF_WIDTH = "half_width"
HALF_HEIGHT = "half_height"

# Default

KEYFRAME_NORMAL_ZERO_FRAME_DEFAULT = {
    POS: (0, 0), 
    ANGLE: 0,
    SCALE: (1, 1),
    ALPHA: 255
}

KEYFRAME_VECTOR_ZERO_FRAME_DEFAULT = {
    POS: (0, 0), 
    ANGLE: 0,
    SCALE: (1, 1),
    ALPHA: 255
}

