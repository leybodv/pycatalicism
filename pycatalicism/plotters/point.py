class Point():
    """
    """

    def __init__(self, x:float, y:float|None, label:str):
        """
        """
        self._x = x
        self._y = y
        self._label = label

    def get_x(self) -> float:
        """
        """
        return self._x

    def get_y(self) -> float|None:
        """
        """
        return self._y
