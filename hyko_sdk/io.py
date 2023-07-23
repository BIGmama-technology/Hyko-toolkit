from enum import Enum
from typing import Any, Union, Optional, Tuple, Callable, Dict, Generator

from pydantic import BaseModel as PBaseModel
from pydantic.fields import ModelField

import numpy as np
from PIL import Image as PIL_Image
import soundfile
import os
import subprocess
import io
from fastapi import HTTPException

from .utils import download_file, upload_file
import uuid
import asyncio
import json
import math


class Image:

    @staticmethod
    def from_ndarray(arr: np.ndarray) -> "Image":
        file = io.BytesIO()
        img = PIL_Image.fromarray(arr)
        img.save(file, format="PNG")
        return Image(bytearray(file.getbuffer().tobytes()), filename="image.png", mime_type="image/png")

    def __init__(self, val: Union["Image", str, uuid.UUID, bytearray], filename: Optional[str] = None, mime_type: Optional[str] = None) -> None:
        self.data: Optional[bytearray] = None
        self.filename: Optional[str] = None
        self.mime_type: Optional[str] = None
        self._task: Optional[asyncio.Task[None]] = None

        if isinstance(val, Image):
            if val.data is not None:
                self._uuid = val._uuid
                self.data = val.data
                self.filename = val.filename
                self.mime_type = val.mime_type
                self._task = val._task
            else:
                raise ValueError("Cannot copy non-synced Image object")

        elif isinstance(val, str):
            self._uuid = uuid.UUID(val).__str__()
            self._task = asyncio.get_running_loop().create_task(self.download())
            return
        
        elif isinstance(val, uuid.UUID):
            self._uuid = val.__str__()
            self._task = asyncio.get_running_loop().create_task(self.download())
            return

        elif isinstance(val, bytearray):
            if filename is None:
                raise ValueError("filename should not be None when creating an Image from bytearray")
            if mime_type is None:
                raise ValueError("mime_type should not be None when creating an Image from bytearray")
            self._uuid = uuid.uuid4().__str__()
            self.data = val
            self.filename = filename
            self.mime_type = mime_type
            self._task = asyncio.get_running_loop().create_task(self.upload())
            return
        
        else:
            raise ValueError(f"Got invalid value type, {type(val)}")

    def __str__(self) -> str:
        return f"{self._uuid}"

    async def download(self):
        metadata_bytes = await download_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/metadata.json")
        metadata = json.loads(metadata_bytes.decode())
        self.filename = metadata["filename"]
        self.mime_type = metadata["type"]
        self.data = bytearray()

        print(f"filename: {self.filename}, type: {self.mime_type}")

        chunks = []

        for idx in range(8):
            chunks.append((idx, bytearray()))

        async def download_chunk(idx: int, data: bytearray):
            data += await download_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/{idx}")

        await asyncio.wait([download_chunk(idx, data) for idx, data in chunks])

        for _, chunk in chunks:
            self.data += chunk


    async def upload(self):
        if self.data is None:
            raise RuntimeError("Can not upload, data should not be None")
        
        if self.filename is None:
            raise RuntimeError("Can not upload, filename should not be None")
        
        if self.mime_type is None:
            raise RuntimeError("Can not upload, mime_type should not be None")
        
        await upload_file(
            url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/metadata.json",
            data=bytearray(json.dumps({"filename": self.filename, "type": self.mime_type}).encode()),
        )

        chunk_size = math.ceil(len(self.data)/8)

        if chunk_size < 256 * 1024:
            chunk_size = 256 * 1024

        cursor_lower = 0

        chunks = []

        for idx in range(8):
            cursor_upper = cursor_lower + chunk_size
            chunks.append((idx, self.data[cursor_lower : cursor_upper]))
            cursor_lower = cursor_upper

        await asyncio.wait([upload_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/{idx}", data=data) for idx, data in chunks])

    async def wait_data(self):
        if self._task is None:
            raise RuntimeError("Data syncing task is None")
        await self._task

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, bytearray], values, config, field):
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

    def to_ndarray(self, keep_alpha_if_png = False) -> np.ndarray:
        if self.data:
            img_bytes_io = io.BytesIO(self.data)
            img = PIL_Image.open(img_bytes_io)
            img = np.asarray(img)
            if keep_alpha_if_png:
                return img
            return img[...,:3]
        else:
            raise HTTPException(
                status_code=500,
                detail="Image decode error"
            )



class Audio:

    @staticmethod
    def from_ndarray(arr: np.ndarray, sampling_rate: int) -> "Audio":
        file = io.BytesIO()
        soundfile.write(file, arr, samplerate=sampling_rate, format="MP3")
        return Audio(bytearray(file.getbuffer().tobytes()), filename="audio.mp3", mime_type="audio/mp3")
    
    def __init__(self, val: Union["Audio", str, uuid.UUID, bytearray], filename: Optional[str] = None, mime_type: Optional[str] = None) -> None:
        self.data: Optional[bytearray] = None
        self.filename: Optional[str] = None
        self.mime_type: Optional[str] = None
        self._task: Optional[asyncio.Task[None]] = None

        if isinstance(val, Audio):
            if val.data is not None:
                self._uuid = val._uuid
                self.data = val.data
                self.filename = val.filename
                self.mime_type = val.mime_type
                self._task = val._task
            else:
                raise ValueError("Cannot copy non-synced Audio object")

        elif isinstance(val, str):
            self._uuid = uuid.UUID(val).__str__()
            self._task = asyncio.get_running_loop().create_task(self.download())
            return
        
        elif isinstance(val, uuid.UUID):
            self._uuid = val.__str__()
            self._task = asyncio.get_running_loop().create_task(self.download())
            return

        elif isinstance(val, bytearray):
            if filename is None:
                raise ValueError("filename should not be None when creating an Audio from bytearray")
            if mime_type is None:
                raise ValueError("mime_type should not be None when creating an Audio from bytearray")
            self._uuid = uuid.uuid4().__str__()
            self.data = val
            self.filename = filename
            self.mime_type = mime_type
            self._task = asyncio.get_running_loop().create_task(self.upload())
            return
        
        else:
            raise ValueError(f"Got invalid value type, {type(val)}")

    def __str__(self) -> str:
        return f"{self._uuid}"

    async def download(self):
        metadata_bytes = await download_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/metadata.json")
        metadata = json.loads(metadata_bytes.decode())
        self.filename = metadata["filename"]
        self.mime_type = metadata["type"]
        self.data = bytearray()

        print(f"filename: {self.filename}, type: {self.mime_type}")

        chunks = []

        for idx in range(8):
            chunks.append((idx, bytearray()))

        async def download_chunk(idx: int, data: bytearray):
            data += await download_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/{idx}")

        await asyncio.wait([download_chunk(idx, data) for idx, data in chunks])

        for _, chunk in chunks:
            self.data += chunk


    async def upload(self):
        if self.data is None:
            raise RuntimeError("Can not upload, data should not be None")
        
        if self.filename is None:
            raise RuntimeError("Can not upload, filename should not be None")
        
        if self.mime_type is None:
            raise RuntimeError("Can not upload, mime_type should not be None")
        
        await upload_file(
            url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/metadata.json",
            data=bytearray(json.dumps({"filename": self.filename, "type": self.mime_type}).encode()),
        )

        chunk_size = math.ceil(len(self.data)/8)

        if chunk_size < 256 * 1024:
            chunk_size = 256 * 1024

        cursor_lower = 0

        chunks = []

        for idx in range(8):
            cursor_upper = cursor_lower + chunk_size
            chunks.append((idx, self.data[cursor_lower : cursor_upper]))
            cursor_lower = cursor_upper

        await asyncio.wait([upload_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/{idx}", data=data) for idx, data in chunks])

    async def wait_data(self):
        if self._task is None:
            raise RuntimeError("Data syncing task is None")
        await self._task

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, bytearray], values, config, field):
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

    _SUBTYPE2DTYPE = {
        "PCM_S8": "int8",
        "PCM_U8": "uint8",
        "PCM_16": "int16",
        "PCM_32": "int32",
        "FLOAT": "float32",
        "DOUBLE": "float64",
    }
    
    def resample(self, sampling_rate: int):
        if self.data and self.filename:
            with open(self.filename, "wb") as f:
                f.write(self.data)
            out = "audio_resampled.mp3"
            if self.filename == out:
                out = "audio_resampled_2.mp3"
                
            subprocess.run(f"ffmpeg -i {self.filename} -ac 1 -ar {sampling_rate} {out} -y".split(" "))
            with open(out, "rb") as f:
                self.data = bytearray(f.read())
                
            os.remove(out)
            
    def convert_to(self, new_ext: str):
        if self.data and self.filename:
            
            # user video.{ext} instead of filename directly to avoid errors with names that has space in it
            file, ext = os.path.splitext(self.filename)
            with open(f"/app/video.{ext}", "wb") as f:
                f.write(self.data)
                
            out = "media_converted." + new_ext 
            if self.filename == out:
                out = "media_converted_2." + new_ext
                
            subprocess.run(f"ffmpeg -i video.{ext} {out} -y".split(" "))
            with open(out, "rb") as f:
                self.data = bytearray(f.read())
                
            os.remove(out)
            
    def to_ndarray(
        self,
        sampling_rate: Optional[int] = None,
        normalize: bool = True,
        frame_offset: int = 0,
        num_frames: int = -1,
    ) -> Tuple[np.ndarray, int]:
        
        if self.data and self.mime_type:
            if "webm" in self.mime_type:
                self.convert_to("mp3")
                
            if sampling_rate:
                self.resample(sampling_rate)
            
            audio_readable = io.BytesIO(self.data)
            with soundfile.SoundFile(audio_readable, "r") as file_:
                if file_.format != "WAV" or normalize:
                    dtype = "float32"
                elif file_.subtype not in Audio._SUBTYPE2DTYPE:
                    raise RuntimeError(f"Unsupported Audio subtype {file_.subtype}")
                else:
                    dtype = Audio._SUBTYPE2DTYPE[file_.subtype]

                frames = file_._prepare_read(frame_offset, None, num_frames)
                waveform: np.ndarray = file_.read(frames, dtype, always_2d=True)
                sample_rate: int = file_.samplerate
                return waveform.reshape((waveform.shape[0])), sample_rate
            
        else:
            raise RuntimeError("Audio decode error (Audio data not loaded)")


class Video:

    def __init__(self, val: Union["Video", str, uuid.UUID, bytearray], filename: Optional[str] = None, mime_type: Optional[str] = None) -> None:
        self.data: Optional[bytearray] = None
        self.filename: Optional[str] = None
        self.mime_type: Optional[str] = None
        self._task: Optional[asyncio.Task[None]] = None

        if isinstance(val, Video):
            if val.data is not None:
                self._uuid = val._uuid
                self.data = val.data
                self.filename = val.filename
                self.mime_type = val.mime_type
                self._task = val._task
            else:
                raise ValueError("Cannot copy non-synced Video object")

        elif isinstance(val, str):
            self._uuid = uuid.UUID(val).__str__()
            self._task = asyncio.get_running_loop().create_task(self.download())
            return
        
        elif isinstance(val, uuid.UUID):
            self._uuid = val.__str__()
            self._task = asyncio.get_running_loop().create_task(self.download())
            return

        elif isinstance(val, bytearray):
            if filename is None:
                raise ValueError("filename should not be None when creating a Video from bytearray")
            if mime_type is None:
                raise ValueError("mime_type should not be None when creating a Video from bytearray")
            self._uuid = uuid.uuid4().__str__()
            self.data = val
            self.filename = filename
            self.mime_type = mime_type
            self._task = asyncio.get_running_loop().create_task(self.upload())
            return
        
        else:
            raise ValueError(f"Got invalid value type, {type(val)}")

    def __str__(self) -> str:
        return f"{self._uuid}"

    async def download(self):
        metadata_bytes = await download_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/metadata.json")
        metadata = json.loads(metadata_bytes.decode())
        self.filename = metadata["filename"]
        self.mime_type = metadata["type"]
        self.data = bytearray()

        print(f"filename: {self.filename}, type: {self.mime_type}")

        chunks = []

        for idx in range(8):
            chunks.append((idx, bytearray()))

        async def download_chunk(idx: int, data: bytearray):
            data += await download_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/{idx}")

        await asyncio.wait([download_chunk(idx, data) for idx, data in chunks])

        for _, chunk in chunks:
            self.data += chunk


    async def upload(self):
        if self.data is None:
            raise RuntimeError("Can not upload, data should not be None")
        
        if self.filename is None:
            raise RuntimeError("Can not upload, filename should not be None")
        
        if self.mime_type is None:
            raise RuntimeError("Can not upload, mime_type should not be None")
        
        await upload_file(
            url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/metadata.json",
            data=bytearray(json.dumps({"filename": self.filename, "type": self.mime_type}).encode()),
        )

        chunk_size = math.ceil(len(self.data)/8)

        if chunk_size < 256 * 1024:
            chunk_size = 256 * 1024

        cursor_lower = 0

        chunks = []

        for idx in range(8):
            cursor_upper = cursor_lower + chunk_size
            chunks.append((idx, self.data[cursor_lower : cursor_upper]))
            cursor_lower = cursor_upper

        await asyncio.wait([upload_file(url=f"https://bpresources.api.wbox.hyko.ai/hyko/{self._uuid}/{idx}", data=data) for idx, data in chunks])

    async def wait_data(self):
        if self._task is None:
            raise RuntimeError("Data syncing task is None")
        await self._task

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, bytearray], values, config, field):
        return cls(value)

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: Dict[str, Any],
        field: Optional[ModelField],
    ):
        if field:
            field_schema["type"] = "string"
            field_schema["format"] = "video"

class BaseModel(PBaseModel):
    class Config:
        json_encoders = {
            Image: lambda v: v._uuid if v else None,
            Audio: lambda v: v._uuid if v else None,
            Video: lambda v: v._uuid if v else None,
        }

# Keep the same
class IOPortType(str, Enum):
    BOOLEAN = "boolean"
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
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
