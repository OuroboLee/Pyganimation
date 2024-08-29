import os
import json
import pygame

from pyganimation._constants import *

class IncompleteAnimationScriptError(Exception):
    def __init__(self):
        self.msg = """
                There are no intermediate frames, or a particular frame does not have the necessary elements for each frame. 
                Check the animation script, and if there is no problem, contact the developer.
        """
    
    def __str__(self):
        return self.msg


class NoZeroFrameInAnimationScriptError(Exception):
    def __init__(self):
        self.msg = """
        Frame 0 is empty, or frame 0 does not have the necessary elements. 
        Check the animation script, and if there is no problem, contact the developer.
        """
    
    def __str__(self):
        return self.msg
    

#############################################################

def load(animation_file_dir):
    with open(animation_file_dir, "r") as anifile:
        return json.load(anifile)
    
def save(animation_file_dir, content):
    with open(animation_file_dir, "w") as anifile:
        os.truncate(animation_file_dir, 0)
        anifile.seek(0)
        json.dump(content, anifile)

def reset(animation_file_dir):
    os.truncate(animation_file_dir, 0)

#############################################################

def get_image_from_script(animation_script, frame_number):
    target = animation_script[frame_number][IMAGE_INFO][TARGET]
    if type(target) == str:
        return pygame.image.load(target)
    
    else:
        if target == ELLIPSE:
            # Ellipse
            return ELLIPSE
        elif target == RECTANGLE:
            # Rectangle
            return RECTANGLE
        elif target == CIRCLE:
            return CIRCLE
        elif target == SQUARE:
            return SQUARE