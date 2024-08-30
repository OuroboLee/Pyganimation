from pyganimation.core.interface.math_interface import IBezierCurveInterface
from pyganimation.core.script_validation_check import _coordinate_validation_check
from itertools import pairwise

class BezierCurve(IBezierCurveInterface):
    def __init__(self,
                 points: list | tuple):
        if type(points) not in (list, tuple):
            raise TypeError("points parameter must be Python list or Python tuple that has more than two coordinate-style values.")
        if len(points) <= 1: 
            raise ValueError("points parameter must be Python list or Python tuple that has more than two coordinate-style values.")
        
        for idx, point in enumerate(points):
            if type(point) not in (list, tuple):
                raise TypeError(f"Invalid point value in index {idx} of points parameter.")
            if len(point) != 2:
                raise ValueError(f"Invalid point value in index {idx} of points parameter.")
            
            for i in point:
                if type(i) not in (int, float):
                    raise ValueError(f"Invalid point value in index {idx} of points parameter.")
                
        
        self._points = points
    
    def _get_final_dot(self, t: float, points: list[tuple]) -> list[tuple] | tuple[float, float]:
        new_points = list()
        for pair in list(pairwise(points)):
            new_points.append(
                (pair[0][0] * (1 - t) + pair[1][0] * t,
                 pair[0][1] * (1 - t) + pair[1][1] * t)
            )

        if len(new_points) > 1:
            return self._get_final_dot(t, new_points)
        else:
            return new_points[0]
        
    def get_dot(self, step: float):
        if type(step) != float:
            raise TypeError("Step must be float type value between 0 and 1.")
        if step < 0 or step > 1:
            raise ValueError("Step must be float type value between 0 and 1.")
        
        return self._get_final_dot(step, self._points)
        
if __name__ == "__main__":
    bezier = BezierCurve([(0, 0), (10, 10), (20, 20)])

    print(bezier.get_dot(0.5))