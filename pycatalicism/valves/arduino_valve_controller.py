from enum import Enum
import threading

class ValveState(Enum):
    """
    State of the solenoid valve
    """
    CLOSE = 0
    OPEN = 1

class ArduinoValveController():
    """
    """

    def __init__(self, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, request_trials:int=3):
        """
        Initialize object with serial connection parameters. Register logger.

        parameters
        ----------
        port:str
            serial port for communication with controller
        baudrate:int
            baudrate to use for communication. Must be the same as in arduino sketch
        bytesize:int
            bytesize to use for communication. Must be the same as in arduino sketch
        parity:str
            parity to use for communication. Must be the same as in arduino sketch
        stopbits:float
            stopbits to use for communication. Must be the same as in arduino sketch
        request_truals:int (default: 3)
            how many times to try connecting to the controller before exception is thrown
        """
        self._port = port
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._read_write_lock = threading.Lock()
        self._logger = valves_logging.get_logger(self.__class__.__name__)
        self._connected = False

    def connect(self):
        """
        """
        response = self._send_message(self._handshake_message)
        state, value = self._parse_response(response)
        if state == 'HSH':
            if value == 'DBQWT':
                self._connected = True
                self._logger.info('Connected to arduino valve controller')
            else:
                raise MessageValueException(f'Unexpected value "{value}" was got from the controller')
        elif  state == 'ERR':
            raise ControllerErrorException(error_code=value)
        else:
            raise MessageStateException(f'Unknown state value "{state}" got from the controller')
