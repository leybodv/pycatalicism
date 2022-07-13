from abc import ABC, abstractmethod

from pycatalicism.chromatograph.chromatograph_status import ChromatographStatus

class Chromatograph(ABC):
    """
    Abstract class representing chromatograph. Subclasses must implement methods connect, start_analysis and get_status
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
    def get_status(self) -> ChromatographStatus:
        """
        Get working status of chromatograph.

        returns
        -------
        chromatograph_status:ChromatographStatus
            status of work of chromatograph
        """
