import os
import sys

import pygame

from pyganimation._constants import *
from pyganimation import AnimationManager, AnimationScript, BaseAnimation
from pyganimation.core.math.bezier_curve import BezierCurve


def main():
    pygame.init()

    screen_width = 1024 ; screen_height = 576; screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Keyframe Script Example")
    clock = pygame.time.Clock()

    current_path = os.path.dirname(__file__)

    example_image_path = os.path.join(current_path, "images\\arrow.png")
    example_image = pygame.image.load(example_image_path)

    fps = 30
    ani_manager = AnimationManager(
        target_screen=screen,
        fps=fps,
        debugging=True
    )
    screen_center = (screen_size[0] / 2, screen_size[1] / 2)

    example_keyframe_script = {
        0: {
            IMAGE_INFO: {
                TARGET: example_image,
                RECT: None
            },
            KEYFRAME_NORMAL_INFO: {
                POS: (400, 400)
            }
        },
        1: {
            KEYFRAME_NORMAL_INFO: {
                POS: (400, 400)
            }
        },
        60: {
            KEYFRAME_NORMAL_INFO: {
                POS: (500, 500),
                ANGLE: 0
            },
            KEYFRAME_INTERPOLATE_INFO: {
                POS: SIN_IN_AND_OUT,
                ANGLE: SIN_IN_AND_OUT
            },
            KEYFRAME_SPECIAL_INFO: {
                POS: FOLLOW_CURVE,
                ANGLE: FOLLOW_CURVE,
                CURVE: BezierCurve([(400, 400), (450, 400), (450, 500), (500, 500)])
            }
        }
    }

    example_script = AnimationScript(example_keyframe_script)
    example_animation = BaseAnimation(
        animation_name = "Example 1",
        animation_script = example_script,
        animation_manager = ani_manager,
        speed = 1,
        loop = -1,
        is_visible = True,
        is_reversed = False
    )

    font_path = os.path.join(current_path, "GodoB.ttf")
    font = pygame.font.Font(font_path)
    FONT_SIZE = 20

    key_a_instruction_text = font.render(
        text="Press A to add animation to animation queue.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )
    key_s_instruction_text = font.render(
        text="Press S to remove animation from animation queue.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )

    key_d_instruction_text = font.render(
        text="Press D to play animation.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )

    key_f_instruction_text = font.render(
        text="Press F to pause animation.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )

    key_g_instruction_text = font.render(
        text="Press G to stop animation.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )

    key_h_instruction_text = font.render(
        text="Press H to replay animation.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )

    key_j_instruction_text = font.render(
        text="Press J to reverse animation.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )

    key_k_instruction_text = font.render(
        text="Press K to show animation.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )

    key_l_instruction_text = font.render(
        text="Press L to hide animation.",
        antialias=True,
        color=pygame.Color("DarkGray") 
    )
    
    instruction_list = [
        key_a_instruction_text,
        key_s_instruction_text,
        key_d_instruction_text,
        key_f_instruction_text,
        key_g_instruction_text,
        key_h_instruction_text,
        key_j_instruction_text,
        key_k_instruction_text,
        key_l_instruction_text
    ]

    # loop
    run = True; fps = 60
    while run:
        dt = clock.tick(fps) / 1000.0

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    example_animation.add()

                elif event.key == pygame.K_s:
                    example_animation.remove()

                elif event.key == pygame.K_d:
                    example_animation.play()

                elif event.key == pygame.K_f:
                    example_animation.pause()

                elif event.key == pygame.K_g:
                    example_animation.stop()
                    
                elif event.key == pygame.K_h:
                    example_animation.replay()

                elif event.key == pygame.K_j:
                    example_animation.reverse()

                elif event.key == pygame.K_k:
                    example_animation.show()

                elif event.key == pygame.K_l:
                    example_animation.hide()

            

        ##### Game & Screen Update #####

        # ingame update
        screen.fill(pygame.Color("#FFFFFF"))

        # Pyganimation Update

        ani_manager.update()
        ani_manager.draw()

        for idx, inst in enumerate(instruction_list):
            screen.blit(inst, (0, idx * FONT_SIZE))

        # pygame screen update
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    sys.exit(main())
