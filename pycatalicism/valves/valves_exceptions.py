class MessageValueException(Exception):
    """
    Exception is thrown when wrong value was got from the controller
    """

class ControllerErrorException(Exception):
    """
    Exception is thrown when controller returns ERR message
    """

    def __init__(self, error_code:str):
        """
        Constructs exception with message specific to error code.

        parameters
        ----------
        error_code:str
            error code in accordance with connection protocol
        """
        if error_code == 'MSGFMT':
            msg = 'Wrong message format'
        elif error_code == 'DVNM':
            msg = 'Wrong device numver'
        elif error_code == 'HNDSHK':
            msg = 'Wrong handshake word'
        elif error_code == 'VL':
            msg = 'Wrong value'
        else:
            msg = 'Unknown error code'
        super().__init__(f'Controller returned error: {msg}')

class MessageStateException(Exception):
    """
    Exception is thrown when unknown state value was got from the controller
    """

class ConnectionException(Exception):
    """
    Exception is thrown when connection problems are encountered
    """
