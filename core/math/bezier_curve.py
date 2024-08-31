from pyganimation.core.interface.math_interface import IBezierCurveInterface
from pyganimation.core.math.tools import is_positive

from itertools import pairwise
from math import atan, degrees

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
        self._delta = 0.001
    
    def _get_final_pos(self, t: float, points: list[tuple]) -> list[tuple] | tuple[float, float]:
        new_points = list()
        for pair in list(pairwise(points)):
            new_points.append(
                (pair[0][0] * (1 - t) + pair[1][0] * t,
                 pair[0][1] * (1 - t) + pair[1][1] * t)
            )

        if len(new_points) > 1:
            return self._get_final_pos(t, new_points)
        else:
            return new_points[0]
        
    def get_pos(self, step: float):
        if type(step) != float:
            raise TypeError("Step must be float type value.")
        
        if step < 0: return self._get_final_pos(0, self._points)

        elif step > 1: return self._get_final_pos(1, self._points)
        
        else: return self._get_final_pos(step, self._points)
    
    def get_angle(self, step: float):
        if type(step) != float:
            raise TypeError("Step must be float type value.")
        
        pos1 = self._get_final_pos(step - self._delta, self._points)
        pos2 = self._get_final_pos(step + self._delta, self._points)

        slope = -(pos2[1] - pos1[1]) / (pos2[0] - pos1[0])

        not_over_half_of_pi = is_positive(pos2[0] - pos1[0])

        # Need to study more about this function.

        return degrees(atan(slope)) if not_over_half_of_pi else degrees(atan(slope)) + 180


        
if __name__ == "__main__":
    bezier = BezierCurve([(0, 0), (10, 10), (30, 20)])

    print(bezier.get_pos(0.5))
    print(bezier.get_angle(0.3))