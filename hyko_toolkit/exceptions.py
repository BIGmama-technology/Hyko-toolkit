from dataclasses import dataclass

from fastapi import status


@dataclass
class APICallError(BaseException):
    status: int
    detail: str = "An api call error happened"


@dataclass
class UtilsCallError(BaseException):
    status: int
    detail: str = "An utility function call error happened"


@dataclass
class OauthTokenExpired(BaseException):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Not authenticated."
