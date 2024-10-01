from pyganimation.core.validation_check.component_validation_check import _image_pathlike_str_validation_check, _frame_number_validation_check
from pyganimation.core.validation_check.normal_validation_check import _image_info_validation_check
from pyganimation._constants import *
import pygame, typing

def mutant1_to_final_script(script: list, debugging: bool = False) -> list:
    total_frame = script[-1] * len(script[:-1]) + 1
    frame_per_image = script[-1]

    if not _frame_number_validation_check(frame_per_image):
        raise ValueError("Invalid frame_per_image value.")

    surfaces = list()
    
    for idx, image in enumerate(script[:-1]):
        for _ in range(frame_per_image + 1 if idx == 0 else frame_per_image):
            surfaces.append(
                construct_surface_tuple(idx, image)
            )

    if debugging:
        print(surfaces)

    return construct_final_script(surfaces, total_frame)

def mutant2_to_final_script(script: list, debugging: bool = False) -> list:
    total_frame = sum(script[-1]) + 1
    frame_per_image_list = script[-1]

    if len(frame_per_image_list) != len(script[:-1]):
        raise ValueError("The length of list for frame_per_image is not same with the number of images.")

    surfaces = list()

    for idx, image in enumerate(script[:-1]):
        frame_per_image = frame_per_image_list[idx]
        if not _frame_number_validation_check(frame_per_image):
            raise ValueError(f"Invalid frame number value in {idx} in list for frame_per_image.")

        for _ in range(frame_per_image + 1 if idx == 0 else frame_per_image):
            surfaces.append(
                construct_surface_tuple(idx, image)
            )

    if debugging:
        print(surfaces)

    return construct_final_script(surfaces, total_frame)

def construct_final_script(surfaces: list, total_frame: int) -> list:
    infos = list()

    for i in range(total_frame): # info
        infos.append(
            {
                RECT: surfaces[i][1],
                POS: (0, 0)
            }
        )
    
    final_script = list()
    for i in range(total_frame):
        final_script.append(
            (surfaces[i][0], infos[i])
        )

    return final_script

def construct_surface_tuple(idx: int, image: typing.Any) -> tuple:
    if type(image) == str:
        if _image_pathlike_str_validation_check(image):
            raise ValueError(f"Invalid pathlike-str for image in idx {idx}.")
            
        surface = pygame.image.load(image)
        rect = None
        
    elif type(image) == pygame.Surface:
        surface = image.copy()
        rect = None

    elif type(image) == dict:
        if not _image_info_validation_check(image):
            raise ValueError(f"Invalid dict-style image info in idx {idx}")

        surface = image[TARGET] if type(image[TARGET]) == pygame.Surface else pygame.image.load(image[TARGET])
        rect = image[RECT]

    else:
        raise ValueError(f"Invalid image in idx {idx}")
    
    surface.set_alpha(255)
    print(surface.get_alpha())

    return (surface, rect)

__all__ = [
    "mutant1_to_final_script",
    "mutant2_to_final_script"
]
