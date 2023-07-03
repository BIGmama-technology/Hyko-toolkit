from .error import BaseError, Errors
from enum import Enum
from typing import Any, Union, Optional, Tuple, Callable, Dict, Generator, List

from pydantic import BaseModel
from pydantic.fields import ModelField

import numpy as np
from PIL import Image as PIL_Image
import base64
import soundfile
import os
import subprocess
import io
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
        img_bytes_io = io.BytesIO(base64_bytes)
        img = PIL_Image.open(img_bytes_io)
        img = np.asarray(img)
        return img, None
    


_SUBTYPE2DTYPE = {
    "PCM_S8": "int8",
    "PCM_U8": "uint8",
    "PCM_16": "int16",
    "PCM_32": "int32",
    "FLOAT": "float32",
    "DOUBLE": "float64",
}

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

    def decode(self, sampling_rate: Optional[int] = None, 
            normalize: bool = True,     
            frame_offset: int = 0,
            num_frames: int = -1,) -> Tuple[Optional[np.ndarray], Optional[int], Optional[BaseError]]:
        
        if len(self.split(",")) != 2:
            return None, None ,Errors.InvalidBase64
        
        header, data = self.split(",")
        if not ("audio" in header) and not ("webm" in header):
            return None, None, Errors.Base64NotAnAudio
        base64_bytes = base64.b64decode(data)

        if os.path.exists("audio.webm"):
            os.remove("audio.webm")
        with open("audio.webm", "wb") as f:
            f.write(base64_bytes)
        if os.path.exists("audio.wav"):
            os.remove("audio.wav")
        if sampling_rate:
            subprocess.run(f"ffmpeg -i audio.webm -ac 1 -ar {sampling_rate} -c:a libmp3lame -q:a 9 audio.wav".split(" "))
        else:
            subprocess.run(f"ffmpeg -i audio.webm audio.wav".split(" "))
        
        with soundfile.SoundFile("audio.wav", "r") as file_:
            if file_.format != "WAV" or normalize:
                dtype = "float32"
            elif file_.subtype not in _SUBTYPE2DTYPE:
                raise ValueError(f"Unsupported subtype: {file_.subtype}")
            else:
                dtype = _SUBTYPE2DTYPE[file_.subtype]

            frames = file_._prepare_read(frame_offset, None, num_frames)
            waveform: np.ndarray = file_.read(frames, dtype, always_2d=True)
            sample_rate: int = file_.samplerate
            return waveform, sample_rate, None
    
    
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


def image_to_base64(image: np.ndarray) -> Image:
    """
    Takes an RGB pixel data as a numpy array and compress it to png and encode it as base64
    """
    img = PIL_Image.fromarray(image) 
    img.save("image.png")
    with open("image.png", "rb") as f:
        data = f.read()
    data = base64.b64encode(data)
    img = Image("data:image/png;base64," + data.decode())
    return img

def audio_to_base64(audio: np.ndarray, sample_rate: int) -> Audio:
    if os.path.exists("audio.wav"):
        os.remove("audio.wav")
    soundfile.write("audio.wav", audio, sample_rate)

    if os.path.exists("audio.webm"):
        os.remove("audio.webm")
    subprocess.run(f"ffmpeg -i audio.wav audio.webm".split(" "))
    with open("audio.webm", "rb") as f:
        data = f.read()
    data = base64.b64encode(data)
    audio = Image("data:video/webm;base64," + data.decode())
    return audio