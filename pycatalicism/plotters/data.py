from pycatalicism.plotters.point import Point

class Data():
    """
    """

    def __init__(self, label:str):
        """
        """
        self._label = label
        self._x = []
        self._y = []

    def add_point(self, point:Point|None):
        """
        """
        if point is None:
            return
        x = point.get_x()
        y = point.get_y()
        if x not in self._x:
            self._x.append(x)
            if y is not None:
                self._y.append(y)
