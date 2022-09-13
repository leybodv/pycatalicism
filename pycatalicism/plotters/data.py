from pycatalicism.plotters.point import Point

class Data():
    """
    Wrapper class for storage of 2-D array of numbers and label. This class is used for non blocking plotting.
    """

    def __init__(self, label:str):
        """
        Instantiates instance variables.

        parameters
        ----------
        label:str
            label to associate with the data
        """
        self._label = label
        self._x = []
        self._y = []

    def add_point(self, point:Point|None):
        """
        Add one point to this data. If point is None, nothing is added. Also, if x value of point is already present in this data, nothing happens. Y value of the point can be None. In this case it is not appended to the data y array.

        parameters
        ----------
        point:Point|None
            point with x and y float values
        """
        if point is None:
            return
        x = point.get_x()
        y = point.get_y()
        if x not in self._x:
            self._x.append(x)
            if y is not None:
                self._y.append(y)

    def get_x(self) -> list[float]:
        """
        Get x values stored in this data object.

        returns
        -------
        x:list[float]
            list of x values
        """
        return self._x

    def get_y(self) -> list[float]:
        """
        Get y values stored in this data object.

        returns
        -------
        y:list[float]
            list of y values
        """
        return self._y

    def get_label(self) -> str:
        """
        Get label associated with this data object.

        returns
        -------
        label:str
            label associated with this data object
        """
        return self._label
