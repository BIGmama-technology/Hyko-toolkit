from pydantic import BaseModel
import enum

class HykoErrorEnum(str, enum.Enum):
    INVALID_BASE_64 = "INVALID_BASE_64",
    NOT_AN_IMAGE = "NOT_AN_IMAGE"
    NOT_AN_AUDIO = "NOT_AN_AUDIO"

class BaseError(BaseModel):
    status: HykoErrorEnum
    message: str

class Errors:
    InvalidBase64 = BaseError(status=HykoErrorEnum.INVALID_BASE_64, message="Provided Base64 string is invalid. (Maybe the header is missing ?)")
    Base64NotAnImage = BaseError(status=HykoErrorEnum.NOT_AN_IMAGE, message="Provided Base64 string does not represent an image")
    Base64NotAnAudio = BaseError(status=HykoErrorEnum.NOT_AN_AUDIO, message="Provided Base64 string does not represent an audio")