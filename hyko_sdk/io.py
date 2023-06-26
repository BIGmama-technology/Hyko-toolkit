from .error import BaseError, Errors
from enum import Enum
from typing import Optional
from pydantic import BaseModel

from typing import Any, Callable, Dict, Generator, Optional

from pydantic import BaseModel
from pydantic.fields import ModelField

from pydantic import BaseModel
import numpy as np
import cv2
import base64
import ffmpeg


class Number(float):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "number"

class Integer(int):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "integer"

class String(str):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "string"


class Image(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return value

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "string"
            field_schema["format"] = "image"

    def decode(self) -> tuple[np.ndarray | None, BaseError | None]:
        if len(self.split(",")) != 2:
            return None, Errors.InvalidBase64
        
        header, data = self.split(",")
        if not ("image" in header):
            return None, Errors.Base64NotAnImage
        base64_bytes = base64.b64decode(data)
        np_bytes = np.frombuffer(base64_bytes, np.uint8)
        img = cv2.imdecode(np_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img, None
    

class AudioMetadata(BaseModel):
    sample_rate: int
    duration: float
    bit_rate: int
    channels: int
    bits_per_sample: int
    bit_rate: int

class Audio(str):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: str, values, config, field):
        return value

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "string"
            field_schema["format"] = "audio"

    def decode(self) -> tuple[np.ndarray | None, AudioMetadata | None, BaseError | None]:
        if len(self.split(",")) != 2:
            return None, None ,Errors.InvalidBase64
        
        header, data = self.split(",")
        if not ("audio" in header):
            return None, None, Errors.Base64NotAnAudio
        base64_bytes = base64.b64decode(data)
        with open("audio.webm", "wb") as f:
            f.write(base64_bytes)
        ffmpeg.input("audio.webm").output("audio.wav").run()

        meta_data: dict = ffmpeg.probe("audio.wav")
        with open("audio.wav", "rb") as f:
            audio = f.read()
        return np.frombuffer(audio, dtype=np.float64), AudioMetadata(**meta_data), None
# Keep the same
class IOPortType(str, Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    IMAGE = "image"
    AUDIO = "audio"
    ARRAY_NUMBER = "array[number]"
    ARRAY_INTEGER = "array[integer]"
    ARRAY_STRING = "array[string]"
    ARRAY_IMAGE = "array[image]"
    ARRAY_AUDIO = "array[audio]"

class IOPort(BaseModel):
    name: str
    description: Optional[str]
    type: IOPortType
    required: bool
    default: Optional[float | int | str]


def image_to_base64(image: np.ndarray) -> tuple[Image, BaseError | None]:
    """
    Takes an RGB pixel data as a numpy array and compress it to png and encode it as base64
    """
    ret, image = cv2.imencode(".png", image)
    
    data = base64.b64encode(image.tobytes())
    img = Image("data:image/png;base64," + data.decode())
    return img, None