from dataclasses import dataclass

from fastapi import status


@dataclass
class CoreExceptionError(Exception):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An api call error happened"

    def __reduce__(self):
        return (CoreExceptionError, (self.status, self.detail))


@dataclass
class APICallError(CoreExceptionError):
    status = status.HTTP_400_BAD_REQUEST
    detail: str = "An api call error happened"


@dataclass
class UtilsCallError(CoreExceptionError):
    status = status.HTTP_400_BAD_REQUEST
    detail: str = "An utility function call error happened"


@dataclass
class OauthTokenExpiredError(CoreExceptionError):
    status = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated."
