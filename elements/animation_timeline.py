from pyganimation.core.script_validation_check import *
from pyganimation.core.interface.animation_script_interface import IAnimationTimelineInterface, IAnimationListInterface
from pyganimation.core.animation_file_manager import load

import pprint

class AnimationTimeline(IAnimationTimelineInterface):
    def __init__(self,
                 script: list | dict | str,
                 debugging: bool = False
                ):
        """
        """
        assert type(script) in (list, dict, str), "Script Parameter must be among path-like str that represents json format file, Python dict, or Python list."

        self._primitive_script = None
        self._script_path = None
        self._debugging = debugging

        if type(script) == str:
            _pathlike_str_validation_check(script)
            
            self._script_path = script
            self._primitive_script = load(script)
        
        else:
            pass
        
        
        self._final_script = dict()





        self._total_frame = 0

    def get_total_frame(self):
        return self._total_frame
    
    def set_total_frame(self, value: int):
        if self._total_frame == 0:
            self._total_frame = value

    def _script_validation_check(self):
        pass

    def timeline_validation_check(self, animation_list: IAnimationListInterface):
        pass

    def __str__(self) -> str:
        return f"<AnimationTimeline Object (Total Frame: {self._total_frame}))>"
    
    def __repr__(self) -> str:
        return pprint.pformat(self._final_script, 4, 300)
    
    def __getitem__(self, key: int) -> dict:
        return self._final_script[key]