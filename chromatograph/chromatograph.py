from abc import ABC, abstractmethod

class Chromatograph(ABC):
    """
    Abstract class representing chromatograph. Subclasses must implement methods connect, set_instrument_method, start_analysis and is_ready_for_analysis
    """

    @abstractmethod
    def connect(self) -> bool:
        """
        Connect to chromatograph.

        returns
        -------
        True if connection was successful
        """

    @abstractmethod
    def set_instrument_method(self, method:str):
        """
        Sets instrument method to specified value

        parameters
        ----------
        method:str
            instrument method which will be started
        """

    @abstractmethod
    def start_analysis(self):
        """
        Start analysis. Subclasses responsible for details of analysis method.
        """

    @abstractmethod
    def is_ready_for_analysis(self) -> bool:
        """
        Check whether chromatograph is ready to start analysis

        returns
        -------
        True if chromatograph is ready for analysis
        """
