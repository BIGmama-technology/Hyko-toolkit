from dataclasses import dataclass

from fastapi import status


@dataclass
class EmailNotValidError(Exception):
    status: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Provided email isn't valid"


@dataclass
class EmailSendError(Exception):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An error ocurred while sending email"


@dataclass
class APICallError(Exception):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An api call error happened"


@dataclass
class OauthTokenExpiredError(Exception):
    status: int = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated."
