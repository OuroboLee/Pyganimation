class FollowableShape():
    def __init__(self):
        """
        The Parent Class for child followable shapes, like BezierCurve, Circle, etc.
        """
        pass

    def get_pos(self, step):
        """
        Should return coordinate value corresponding the parameter step.
        Should be overrided by child class.

        :param step:
        """
        pass

    def get_angle(self, step):
        """
        Should return angle value corresponding the parameter step.
        Should be overrided by child class.

        :param step:
        """
        pass