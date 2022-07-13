from abc import ABC, abstractmethod

class Chromatograph(ABC):
    """
    Abstract class representing chromatograph. Subclasses must implement methods connect, start_analysis and is_ready_for_analysis
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
