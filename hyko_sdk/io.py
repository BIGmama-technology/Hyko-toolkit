from .error import BaseError, Errors
from enum import Enum
from typing import Any, Union, Optional, Tuple, Callable, Dict, Generator, List

from pydantic import BaseModel
from pydantic.fields import ModelField

import numpy as np
import cv2
import base64
import torchaudio
import os
import subprocess

class Boolean(int):
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
            field_schema["type"] = "boolean"

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
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "string"
            field_schema["format"] = "image"

    def decode(self) -> Tuple[Optional[np.ndarray], Optional[BaseError]]:
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
    
class Audio(str):

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
            field_schema["format"] = "audio"

    def decode(self, sampling_rate: Optional[int]  = None) -> Tuple[Optional[np.ndarray], Optional[int], Optional[BaseError]]:
        if len(self.split(",")) != 2:
            return None, None ,Errors.InvalidBase64
        
        header, data = self.split(",")
        if not ("audio" in header) or not ("webm" in header):
            return None, None, Errors.Base64NotAnAudio
        base64_bytes = base64.b64decode(data)
        with open("audio.webm", "wb") as f:
            f.write(base64_bytes)
        if os.path.exists("audio.wav"):
            os.remove("audio.wav")
        if sampling_rate:
            subprocess.run(f"ffmpeg -i audio.webm -ac 1 -ar {sampling_rate} -c:a libmp3lame -q:a 9 audio.wav".split(" "))
        else:
            subprocess.run(f"ffmpeg -i audio.webm -o audio.wav".split(" "))
        

        waveform, sample_rate = torchaudio.load("audio.wav")
        return waveform.numpy()[0], sample_rate, None
    
    
# Keep the same
class IOPortType(str, Enum):
    BOOLEAN = "boolean"
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
    default: Optional[Union[float, int, str]]


def image_to_base64(image: np.ndarray) -> Tuple[Image, Optional[BaseError]]:
    """
    Takes an RGB pixel data as a numpy array and compress it to png and encode it as base64
    """
    ret, image = cv2.imencode(".png", image)
    
    data = base64.b64encode(image.tobytes())
    img = Image("data:image/png;base64," + data.decode())
    return img, None

