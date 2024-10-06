import os
import sys

import pygame

from pyganimation._constants import *
from pyganimation import AnimationManager, SpriteAnimationScript, BaseAnimation


def main():
    pygame.init()

    screen_width = 1024 ; screen_height = 576; screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Keyframe Script Example")
    clock = pygame.time.Clock()

    current_path = os.path.dirname(__file__)

    example_image_path = os.path.join(current_path, "images\\xmasgirl1.png")
    example_image = pygame.image.load(example_image_path)

    fps = 30
    ani_manager = AnimationManager(
        target_screen=screen,
        fps=fps,
        debugging=True
    )

    example_keyframe_script = [
        {
            TARGET: example_image,
            RECT: (32 * 0, 0, 32, 48)
        },
        {
            TARGET: example_image,
            RECT: (32 * 1, 0, 32, 48)
        },
        {
            TARGET: example_image,
            RECT: (32 * 2, 0, 32, 48)
        },
        {
            TARGET: example_image,
            RECT: (32 * 3, 0, 32, 48)
        },
        10
    ]

    example_script = SpriteAnimationScript(example_keyframe_script, True)
    example_animation = BaseAnimation(
        animation_name = "Example 1",
        animation_script = example_script,
        animation_manager = ani_manager,
        speed = 2,
        loop = -1,
        is_visible = True,
        is_reversed = False
    )
    example_animation.update_animation_info(ABS_POS, (screen_width // 2, screen_height // 2))

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
