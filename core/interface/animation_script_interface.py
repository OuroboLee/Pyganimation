from abc import ABCMeta, abstractmethod
from typing import Any

class IAnimationScriptStyleBaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self,
                 script: str | dict | list,
                 debugging: bool = False):
        """
        """
        pass

    @abstractmethod
    def _dict_or_list_style_script_process(self, script: dict | list) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __getitem__(self, key: Any) -> dict:
        pass

class IAnimationScriptInterface(IAnimationScriptStyleBaseInterface, metaclass=ABCMeta):
    @abstractmethod
    def _normal_vector_script_validation_check(self, script: dict) -> None:
        """
        """
        pass

    @abstractmethod
    def _keyframe_vector_script_validation_check(self, script: dict) -> None:
        """
        """
        pass
    
    @abstractmethod
    def _normal_normal_script_validation_check(self, script: dict) -> None:
        """
        """
        pass

    @abstractmethod
    def _keyframe_normal_script_validation_check(self, script: dict) -> None:
        """
        """
        pass

    @abstractmethod
    def _image_info_validation_check(image_info: dict, frame_num: int) -> None:
        """
        """
        pass
    
    @abstractmethod
    def _shape_info_validation_check(shape_info: dict, frame_num: int) -> None:
        """
        """
        pass
    
    @abstractmethod
    def _normal_normal_info_validation_check(normal_info: dict, frame_num: int) -> None:
        """
        """
        pass

    @abstractmethod
    def _keyframe_normal_info_validation_check(normal_info: dict, frame_num: int) -> None:
        """
        """
        pass

    @abstractmethod
    def _normal_vector_info_validation_check(normal_info: dict, shape_target: str, frame_num: int) -> None:
        """
        """
        pass

    @abstractmethod
    def _keyframe_vector_info_validation_check(keyframe_info: dict, shape_target: str, frame_num: int) -> None:
        """
        """
        pass

    @abstractmethod
    def get_total_frame(self):
        """
        """
        pass

    @abstractmethod
    def get_script_type(self):
        """
        """
        pass

class IAnimationTimelineInterface(IAnimationScriptStyleBaseInterface, metaclass=ABCMeta):
    @abstractmethod
    def _script_validation_check(self):
        """
        """
        pass

    @abstractmethod
    def timeline_validation_check(self, animation_list):
        """
        """
        pass

    @abstractmethod
    def get_total_frame(self):
        """
        """
        pass

    @abstractmethod
    def set_total_frame(self, value: int) -> None:
        """
        """
        pass

class IAnimationListInterface(IAnimationScriptStyleBaseInterface, metaclass=ABCMeta):
    @abstractmethod
    def _script_validation_check(self):
        """
        """
        pass

    @abstractmethod
    def get_name_list(self):
        """
        """
        pass

class ISpriteAnimationScriptInterface(IAnimationScriptStyleBaseInterface, metaclass=ABCMeta):
    @abstractmethod
    def get_total_frame(self):
        pass

__all__ = [
    "IAnimationScriptInterface",
    "IAnimationListInterface",
    "IAnimationTimelineInterface",
    "ISpriteAnimationScriptInterface"
]

    
        