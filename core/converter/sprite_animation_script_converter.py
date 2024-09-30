from pyganimation._constants import RECT, POS

def mutant1_to_final_script(script: list, debugging: bool = False) -> list:
    total_frame = script[-1] * len(script[:-1]) + 1

    surfaces = list()

    return construct_final_script(surfaces, total_frame)

def mutant2_to_final_script(script: list, debugging: bool = False) -> list:
    total_frame = None

    surfaces = list()

    return construct_final_script(surfaces, total_frame)

def construct_final_script(surfaces: list, total_frame: int) -> list:
    infos = list()

    for _ in range(total_frame): # info
        infos.append(
            {
                RECT: None,
                POS: (0, 0)
            }
        )
    
    final_script = list()
    for i in range(total_frame):
        final_script.append(
            (surfaces[i], infos[i])
        )

    return final_script