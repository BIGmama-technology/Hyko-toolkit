from dataclasses import dataclass


@dataclass
class APICallError(BaseException):
    status: int
    detail: str = "An api call error happened"
