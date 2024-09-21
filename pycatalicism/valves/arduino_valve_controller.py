from enum import Enum
import threading
import time

import serial

import pycatalicism.valves.valves_logging as valves_logging
from pycatalicism.valves.valves_exceptions import MessageValueException
from pycatalicism.valves.valves_exceptions import ControllerErrorException
from pycatalicism.valves.valves_exceptions import MessageStateException
from pycatalicism.valves.valves_exceptions import ConnectionException

class ValveState(Enum):
    """
    State of the solenoid valve
    """
    CLOSE = 0
    OPEN = 1

class ArduinoValveController():
    """
    """

    def __init__(self, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, logfilename:str, request_trials:int=3):
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
        logfilename:str
            path to file to write logs to
        request_truals:int (default: 3)
            how many times to try connecting to the controller before exception is thrown
        """
        self._port = port
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._read_write_lock = threading.Lock()
        self._logger = valves_logging.get_logger(self.__class__.__name__, logfilename)
        self._request_trials = request_trials
        self._handshake_command = 'HSH'
        self._handshake_value = 'NISMF'
        self._set_state_command = 'SET'
        self._get_state_command = 'GET'
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
        if not self._connected:
            raise ConnectionException('Connect to controller first')
        value = "OPEN" if state == ValveState.OPEN else "CLOSE"
        response = self._send_message(command=self._set_state_command, devnum=valve_num, value=value)
        controller_state, controller_value = self._parse_response(response)
        if controller_state == 'OK':
            self._logger.info(f'Successfully set valve {valve_num} to {value}')
            return
        elif controller_state == 'ERR':
            raise ControllerErrorException(error_code=controller_value)
        else:
            raise MessageStateException(f'Unknown state value "{controller_state}" got from the controller')

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
        if not self._connected:
            raise ConnectionException('Connect to controller first')
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

    def _send_message(self, command:str, devnum:int, value:str) -> str:
        """
        Sends message to the controller and gets answer from it. Message is made up according to the connection protocol.

        parameters
        ----------
        command:str
            command to send to the controller
        devnum:int
            number of valve to send to the controller
        value:str
            value to send to the controller

        returns
        -------
        ans:str
            answer from the controller in a format: @devstat.value#
        """
        with self._read_write_lock:
            with serial.Serial(port=self._port, baudrate=self._baudrate, bytesize=self._bytesize, parity=self._parity, stopbits=self._stopbits, timeout=1) as ser:
                for i in range(self._request_trials):
                    msg = f'@{command}.{devnum}.{value}#'.encode(encoding='ascii')
                    self._logger.log(level=5, msg=f'Writing message: {msg}')
                    ser.write(msg)
                    time.sleep(0.05)
                    ans = ser.read_until(expected='#'.encode(encoding='ascii'))
                    self._logger.log(level=5, msg=f'Got byte answer: {ans}')
                    ans = str(ans, encoding='ascii')
                    self._logger.log(level=5, msg=f'String answer: {ans}')
                    if ans.startswith('@') and ans.endswith('#') and ans.find('.') > 0 and ans.find('.') < ans.find('#'):
                        return ans
                    else:
                        self._logger.warning(f'Wrong message was got from the controller: {ans}. Trying to connect again. Trial #{i}.')
        raise ConnectionException(f'Wrong message was got from the controller after {self._request_trials} times.')

    def _parse_response(self, response:str) -> tuple[str, str]:
        """
        Parse answer from the controller according to connection protocol.

        parameters
        ----------
        response:str
            response message got from the controller

        returns
        -------
        state:str
            state part of the message
        value:str
            value part of the message
        """
        split = response.split(sep='.')
        state = split[0].removeprefix('@')
        value = split[1].removesuffix('#')
        return (state, value)
