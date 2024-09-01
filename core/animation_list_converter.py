from pyganimation.core.interface.animation_interface import IAnimationBaseInterface
from pyganimation.elements import BaseAnimation, BaseVectorAnimation, Animation

def list_mutant_1_to_default(script: list):
    result_dict = dict()

    for animation in script:
        if not isinstance(animation, IAnimationBaseInterface):
            raise ValueError("Invalid animation list: the objects in list must be Animation / BaseAnimation / BaseVectorAnimation instance.")
        
        anim_dict = dict()

        if type(animation) == BaseAnimation:
            pass

        elif type(animation) == BaseVectorAnimation:
            pass

        elif type(animation) == Animation:
            pass

