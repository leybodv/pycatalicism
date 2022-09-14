class Point():
    """
    Wrapper class to store 2D data point. Used by non-blocking plotter to send and receive data through multiprocessing pipe.
    """

    def __init__(self, x:float, y:float|None, label:str):
        """
        Initialize instance variables.

        parameters
        ----------
        x:float
            x coordinate
        y:float|None
            y coordinate, None means that this is 1D data
        label:str
            label to associate with the data
        """
        self._x = x
        self._y = y
        self._label = label

    def get_x(self) -> float:
        """
        Get x value.

        returns
        -------
        x:float
            x value
        """
        return self._x

    def get_y(self) -> float|None:
        """
        Get y value.

        returns
        -------
        y:float
            y value
        """
        return self._y

    def get_label(self) -> str:
        """
        Get label associated with data.

        returns
        -------
        label:str
            label associated with data
        """
        return self._label
