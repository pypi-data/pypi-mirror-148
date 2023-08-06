"""Includes classes and functions related to errors (and error handling)

Note: Basically every other module in this package (Smg88) depends on this one :) no pressure self
"""


from types import EllipsisType
from typing import Dict


class ErrorHandle():
    """Class that handles errors the user can identify / recover from
    """

    handleName = "Generic Error Handle: "

    def __init__(cls, msg, *msgs, **extra):
        msg = str(msg)
        _msgs = [str(m) for m in msgs]
        _msgs = '\n'.join(_msgs)
        cls.msg = f"{cls.handleName}\n{msg}\n{_msgs}"
        cls.extras = extra

    def __str__(self):
        return f"{self.msg}"


class UserErrorHandle(ErrorHandle):
    handleName = "User Error Handle: "


class ProgrammerErrorHandle(ErrorHandle):
    handleName = "Programmer Error Handle: "


class Error(Exception):
    """Exception class that is root of all custom exceptions
    """

    msg: str
    extra: Dict
    errorHandle: ErrorHandle

    def __init__(self, msg, *msgs, errorHandle: ErrorHandle | EllipsisType = ..., **extra):
        msg = str(msg)
        _msgs: str = '\n'.join([str(m) for m in msgs])
        self.msg = f"Message: \n{msg}\n{_msgs}"
        self.extras = extra
        self.errorHandle = errorHandle  # type: ignore

    def __str__(self):
        return f"{self.msg}\n" + "\n".join(f"{k}: {v}" for k, v in self.extras.items()) + f"\n{str(self.errorHandle)}"


class SafeCatchAll(Error, Exception):
    """e.g. >>> catch SafeCatchAll as e: SafeCatchAll(e); foo(); bar(); Use to catch all non-program-terminating exceptions (like KeyboardInterrupt)



    This is to allow for a custom error deriving from errors.Error to indicate a system shutdown and not have to change any code

    """
    @staticmethod
    def __call__(err: BaseException):
        if isinstance(err, KeyboardInterrupt):
            raise err
        elif isinstance(err, SystemExit):
            raise err


class ProgrammerError(Error):
    """Exception class that is root of all internal / implementation / programmer related errors
    """
    ...


class InappropriateRequest(ProgrammerError):
    """Exception class that is raised when a request on some programming object / function / property is inappropriate
    """
    ...


class SimpleUserError(Error):
    """Error class used to refer to errors that are not programmer errors

    Args:
        Error (str / strings): Represents the error message and attached error handles
        *errorHandle (ErrorHandle): Represents the error handle that is attached to the error
    """
    ...
