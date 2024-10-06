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

    def __str__(self) -> str:
        return f"rect={self.rect}, scale={self.scale} - {self.scale_anchor}, angle={self.angle} - {self.angle_anchor}"
    
__all__ = ["Anchor"]

if __name__ == "__main__":
    from pyganimation import CENTER
    anchor = Anchor(
        CENTER, CENTER, pygame.Rect(0, 0, 32, 48),
        scale=(1, 1), angle=0
    )

    current_pos = (512, 288)
    print(current_pos, anchor.modify_pos(current_pos))