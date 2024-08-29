import os
import sys

import pygame
from pygame import Rect
import pygame_gui
from pygame_gui.elements import *
from pygame_gui import UIManager

from pyganimation import AnimationManager

from pyganimation import BaseAnimation
from pyganimation._constants import *
from pyganimation import AnimationScript

def main():
    pygame.init()

    screen_width = pygame.display.get_desktop_sizes()[0][0] ; screen_height = pygame.display.get_desktop_sizes()[0][1]
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("")
    clock = pygame.time.Clock()

    current_path = os.path.dirname(__file__)

    # pygame_gui base
    manager = UIManager((screen_width, screen_height))

    stop_button = UIButton(
        relative_rect = Rect(10, screen_height - 60, 50, 50),
        text = "STOP",
        manager = manager
    )

    pause_button = UIButton(
        relative_rect = Rect(70, screen_height - 60, 50, 50),
        text = "PAUSE",
        manager = manager
    )

    play_button = UIButton(
        relative_rect = Rect(130, screen_height - 60, 50, 50),
        text = "PLAY",
        manager = manager
    )

    replay_button = UIButton(
        relative_rect = Rect(190, screen_height - 60, 50, 50),
        text = "REPLAY",
        manager = manager
    )

    add_button = UIButton(
        relative_rect = Rect(250, screen_height - 60, 50, 50),
        text = "ADD",
        manager = manager
    )

    remove_button = UIButton(
        relative_rect = Rect(310, screen_height - 60, 50, 50),
        text = "REMOVE",
        manager = manager
    )

    reverse_button = UIButton(
        relative_rect = Rect(370, screen_height - 60, 50, 50),
        text = "REV",
        manager = manager
    )

    show_button = UIButton(
        relative_rect = Rect(430, screen_height - 60, 50, 50),
        text = "SHOW",
        manager = manager
    )

    hide_button = UIButton(
        relative_rect = Rect(490, screen_height - 60, 50, 50),
        text = "HIDE",
        manager = manager
    )

    # pymunk base

    # pyganimation base
    fps = 30
    ani_manager = AnimationManager(screen, fps, True)

    test_img_path = os.path.join(current_path, "test_img.png")

    keyframe_script = {
        0: {
            IMAGE_INFO: {
                TARGET: test_img_path,
                RECT: None
            },
            KEYFRAME_NORMAL_INFO: {
                POS: (400, 400)
            }
        },
        60: {
            KEYFRAME_NORMAL_INFO: {
                ANGLE: 60
            },
            KEYFRAME_INTERPOLATE_INFO: {
                ANGLE: EXPO_IN
            }
        },
        120: {
            KEYFRAME_NORMAL_INFO: {
                ANGLE: 0
            },
            KEYFRAME_INTERPOLATE_INFO: {
                ANGLE: EXPO_OUT,
                ANGLE_ANCHOR: BOTTOMLEFT
            }
        }
    }

    test_script = AnimationScript(keyframe_script, debugging=True)
    test_ani = BaseAnimation("test animation", test_script, ani_manager, 
                             loop = -1,
                             speed = 3,
                             is_instant_removed_from_animation_queue_after_animation_ends=True
                            )
    test_ani.update_animation_info(ABS_ANGLE, -60)

    # loop
    run = True
    while run:
        dt = clock.tick(fps) / 1000.0

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if test_ani._is_playing:
                    test_ani.pause()
                else:
                    test_ani.play()

            manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == stop_button:
                    test_ani.stop()

                elif event.ui_element == pause_button:
                    test_ani.pause()

                elif event.ui_element == play_button:
                    test_ani.play()

                elif event.ui_element == replay_button:
                    test_ani.replay()

                elif event.ui_element == add_button:
                    test_ani.add()
                
                elif event.ui_element == remove_button:
                    test_ani.remove()

                elif event.ui_element == reverse_button:
                    test_ani.reverse()

                elif event.ui_element == hide_button:
                    test_ani.hide()

                elif event.ui_element == show_button:
                    test_ani.show()

        ##### Game & Screen Update #####

        # ingame update
        screen.fill(pygame.Color("#FFFFFF"))

        # pygame_gui manager update
        manager.update(dt)
        manager.draw_ui(screen)

        # pymunk update

        # pyganimation update
        ani_manager.update()
        ani_manager.draw()
        
        # pygame screen update
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    sys.exit(main())