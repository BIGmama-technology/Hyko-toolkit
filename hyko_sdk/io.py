import io
import os
import subprocess
from typing import Any, Optional
from uuid import UUID, uuid4

import numpy as np
import soundfile  # type: ignore
from numpy.typing import NDArray
from PIL import Image as PIL_Image
from pydantic import (
    GetJsonSchemaHandler,
    field_validator,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from hyko_sdk.metadata import CoreModel
from hyko_sdk.types import MimeType

GLOBAL_STORAGE_PATH = "/app/storage"


class HykoBaseType(CoreModel):
    file_name: str

    @field_validator("file_name")
    @classmethod
    def validate_file_name(cls, file_name: str):
        obj_id, obj_mime = os.path.splitext(file_name)
        obj_id = UUID(obj_id)
        obj_mime = MimeType(obj_mime.lstrip("."))
        return file_name

    def get_name(self) -> str:
        return self.file_name

    def get_mime(self) -> MimeType:
        _, obj_mime = os.path.splitext(self.file_name)
        obj_mime = MimeType(obj_mime.lstrip("."))
        return obj_mime

    def save(self, obj_data: bytes) -> None:
        """save obj to file system"""
        with open(os.path.join(GLOBAL_STORAGE_PATH, self.file_name), "wb") as f:
            f.write(obj_data)

    def get_data(self) -> bytes:
        """read from file system"""
        with open(os.path.join(GLOBAL_STORAGE_PATH, self.file_name), "rb") as f:
            obj = f.read()

        return obj

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema["type"] = cls.__name__.lower()

        return json_schema


class Image(HykoBaseType):
    @field_validator("file_name")
    @classmethod
    def mime_validator(cls, file_name: str):
        _, obj_mime = os.path.splitext(file_name)
        if obj_mime.lstrip(".") not in [MimeType.PNG.value, MimeType.JPEG.value]:
            raise ValueError("Invalid mime for image")
        return file_name

    def __init__(
        self,
        obj_mime: MimeType = MimeType.PNG,
        file_name: Optional[str] = None,
        val: Optional[bytes] = None,
    ):
        if not file_name:
            obj_id = uuid4()
            file_name = str(obj_id) + "." + obj_mime.value

        super().__init__(file_name=file_name)

        if val:
            self.save(val)

    @staticmethod
    def from_ndarray(
        arr: np.ndarray[Any, Any],
        encoding: MimeType = MimeType.PNG,
    ) -> "Image":
        file = io.BytesIO()
        img = PIL_Image.fromarray(arr)  # type: ignore
        img.save(file, format=encoding.value)

        return Image(
            val=file.getbuffer().tobytes(),
            obj_mime=encoding,
        )

    @staticmethod
    def from_pil(
        img: PIL_Image.Image,
        encoding: MimeType = MimeType.PNG,
    ) -> "Image":
        file = io.BytesIO()
        img.save(file, format=encoding.value)

        return Image(
            val=file.getbuffer().tobytes(),
            obj_mime=encoding,
        )

    def to_ndarray(self, keep_alpha_if_png: bool = False) -> NDArray[Any]:
        if self.get_data():
            img_bytes_io = io.BytesIO(self.get_data())
            img = PIL_Image.open(img_bytes_io)
            img = np.asarray(img)
            if keep_alpha_if_png:
                return img
            return img[..., :3]
        else:
            raise RuntimeError("Image decode error (Image data not loaded)")

    def to_pil(self) -> PIL_Image.Image:
        img_bytes_io = io.BytesIO(self.get_data())
        img = PIL_Image.open(img_bytes_io)
        return img


class Audio(HykoBaseType):
    @field_validator("file_name")
    @classmethod
    def mime_validator(cls, file_name: str):
        _, obj_mime = os.path.splitext(file_name)
        if obj_mime.lstrip(".") not in [
            MimeType.MPEG.value,
            MimeType.WEBM.value,
            MimeType.WAV.value,
            MimeType.MP3.value,
        ]:
            raise ValueError("Invalid mime for Audio")
        return file_name

    def __init__(
        self,
        obj_mime: MimeType = MimeType.MP3,
        file_name: Optional[str] = None,
        val: Optional[bytes] = None,
    ):
        if not file_name:
            obj_id = uuid4()
            file_name = str(obj_id) + "." + obj_mime.value

        super().__init__(file_name=file_name)

        if val:
            self.save(val)

    @staticmethod
    def from_ndarray(arr: np.ndarray[Any, Any], sampling_rate: int) -> "Audio":
        file = io.BytesIO()
        soundfile.write(file, arr, samplerate=sampling_rate, format="MP3")  # type: ignore
        return Audio(
            val=file.getbuffer().tobytes(),
            obj_mime=MimeType.MP3,
        )

    def convert_to(self, new_ext: MimeType):
        out = "audio_converted." + new_ext.value

        subprocess.run(
            f"ffmpeg -i {os.path.join(GLOBAL_STORAGE_PATH, self.file_name)} {out} -y".split(
                " "
            )
        )
        with open(out, "rb") as f:
            data = f.read()
        os.remove(out)

        return Audio(val=data, obj_mime=new_ext)

    def to_ndarray(  # type: ignore
        self,
        frame_offset: int = 0,
        num_frames: int = -1,
    ):
        new_audio = self.convert_to(MimeType.MP3)

        audio_readable = io.BytesIO(new_audio.get_data())

        with soundfile.SoundFile(audio_readable, "r") as file_:
            frames = file_._prepare_read(frame_offset, None, num_frames)  # type: ignore
            waveform: np.ndarray = file_.read(frames, "float32", always_2d=True)  # type: ignore
            sample_rate: int = file_.samplerate

        return waveform, sample_rate  # type: ignore


class Video(HykoBaseType):
    @field_validator("file_name")
    @classmethod
    def mime_validator(cls, file_name: str):
        _, obj_mime = os.path.splitext(file_name)
        if obj_mime.lstrip(".") not in [
            MimeType.WEBM.value,
            MimeType.MP4.value,
        ]:
            raise ValueError("Invalid mime for Audio")
        return file_name

    def __init__(
        self,
        obj_mime: MimeType = MimeType.MP4,
        file_name: Optional[str] = None,
        val: Optional[bytes] = None,
    ):
        if not file_name:
            obj_id = uuid4()
            file_name = str(obj_id) + "." + obj_mime.value

        super().__init__(file_name=file_name)

        if val:
            self.save(val)


class PDF(HykoBaseType):
    @field_validator("file_name")
    @classmethod
    def mime_validator(cls, file_name: str):
        _, obj_mime = os.path.splitext(file_name)
        if obj_mime.lstrip(".") not in [
            MimeType.PDF.value,
        ]:
            raise ValueError("Invalid mime for Audio")
        return file_name

    def __init__(
        self,
        obj_mime: MimeType = MimeType.PDF,
        file_name: Optional[str] = None,
        val: Optional[bytes] = None,
    ):
        if not file_name:
            obj_id = uuid4()
            file_name = str(obj_id) + "." + obj_mime.value

        super().__init__(file_name=file_name)

        if val:
            self.save(val)


class CSV(HykoBaseType):
    @field_validator("file_name")
    @classmethod
    def mime_validator(cls, file_name: str):
        _, obj_mime = os.path.splitext(file_name)
        if obj_mime.lstrip(".") not in [
            MimeType.CSV.value,
        ]:
            raise ValueError("Invalid mime for Audio")
        return file_name

    def __init__(
        self,
        obj_mime: MimeType = MimeType.CSV,
        file_name: Optional[str] = None,
        val: Optional[bytes] = None,
    ):
        if not file_name:
            obj_id = uuid4()
            file_name = str(obj_id) + "." + obj_mime.value

        super().__init__(file_name=file_name)

        if val:
            self.save(val)
