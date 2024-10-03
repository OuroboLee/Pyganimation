from pyganimation.core.interface.math_interface import IAnchorInterface

from pyganimation.core.math.interpolate_functions import scale_anchor_interpret, angle_anchor_interpret
import pygame

class Anchor(IAnchorInterface):
    def __init__(self, scale_anchor, angle_anchor, rect: pygame.Rect, scale: tuple, angle: int | float):
        """
        Creates an anchor collection object with target_script.
        """
        self.scale_anchor = scale_anchor
        self.angle_anchor = angle_anchor
        self.rect = rect
        self.scale = scale
        self.angle = angle

    def modify_pos(self, pos: tuple) -> tuple:
        modified_pos = scale_anchor_interpret(
            self.scale_anchor, self.rect,
            pos, self.scale
        )

        modified_pos = angle_anchor_interpret(
            self.angle_anchor, self.rect,
            pos, self.scale, self.angle
        )

        return modified_pos
    
__all__ = ["Anchor"]