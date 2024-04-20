from dataclasses import dataclass


@dataclass
class APICallError(BaseException):
    status: int
    detail: str = "An api call error happened"


@dataclass
class UtilsCallError(BaseException):
    status: int
    detail: str = "An utility function call error happened"
