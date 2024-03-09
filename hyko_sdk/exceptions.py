from dataclasses import dataclass


@dataclass
class BuildError(BaseException):
    function_name: str
    message: str


@dataclass
class PushError(BaseException):
    function_name: str
    message: str


@dataclass
class LoginError(BaseException):
    function_name: str
    message: str
