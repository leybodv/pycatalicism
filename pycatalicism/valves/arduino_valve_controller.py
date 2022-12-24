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
        Connect to the valve controller. Methods sends handshake message to the controller and checks the response.
        """
        response = self._send_message(command=self._handshake_command, devnum=1, value=self._handshake_value)
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

    def set_state(self, valve_num:int, state:ValveState):
        """
        Set state of the valve.

        parameters
        ----------
        valve_num:int
            Valve number from 1 to 5
        state:ValveState
            Whether to open or close the valve
        """
        value = "OPEN" if state == ValveState.OPEN else "CLOSE"
        response = self._send_message(command=self._set_state_command, devnum=valve_num, value=value)
        state, value = self._parse_response(response)
        if state == 'OK':
            self._logger.info(f'Successfully set valve {valve_num} to {state}')
            return
        elif state == 'ERR':
            raise ControllerErrorException(error_code=value)
        else:
            raise MessageStateException(f'Unknown state value "{state}" got from the controller')

    def get_state(self, valve_num:int) -> ValveState:
        """
        Retrieve state of the valve from the controller.

        parameters
        ----------
        valve_num:int
            Valve number from 1 to 5

        returns
        -------
        state:ValveState
            whether the valve is opened or closed
        """
        response = self._send_message(command=self._get_state_command, devnum=valve_num, value="NONE")
        state, value = self._parse_response(response)
        if state == 'ANS':
            if value == 'OPEN':
                self._logger.info(f'Valve {valve_num} is opened')
                return ValveState.OPEN
            elif value == 'CLOSE':
                self._logger.info(f'Valve {valve_num} is closed')
                return ValveState.CLOSE
            else:
                raise MessageValueException(f'Unexpected value "{value}" was got from the controller')
        elif state == 'ERR':
            raise ControllerErrorException(error_code=value)
        else:
            raise MessageStateException(f'Unknown state value "{state}" was got from the controller')
