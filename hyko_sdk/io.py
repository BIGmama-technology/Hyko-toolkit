import asyncio
import io
import os
import subprocess
import uuid
from enum import Enum
from typing import Any, Literal, Optional, Self, Tuple, Union
from uuid import UUID

import numpy as np
import soundfile  # type: ignore
from numpy.typing import NDArray
from PIL import Image as PIL_Image
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema

from hyko_sdk.types import PyObjectId, StorageObject, StorageObjectType
from hyko_sdk.utils import ObjectStorageConn


class HykoBaseType:
    _obj_id: Optional[UUID] = None
    _obj: Optional[StorageObject] = None
    _sync_conn: Optional[ObjectStorageConn] = None
    _sync_tasks: Optional[list[asyncio.Task[None]]] = None

    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, Self],
    ) -> None:
        if isinstance(val, HykoBaseType):
            self._obj = val._obj
            self._obj_id = val._obj_id
            self.sync_storage()
            return

        if isinstance(val, uuid.UUID):
            self._obj_id = val
            self.sync_storage()
            return

        if isinstance(val, str):
            self._obj_id = UUID(val)
            self.sync_storage()
            return

    @classmethod
    def validate_from_id(cls, value: Union[str, UUID]) -> Self:
        ...

    @classmethod
    def validate_from_object(
        cls,
        value: Union[tuple[bytearray, str, str], Self],
    ) -> Self:
        ...

    @classmethod
    def set_sync(
        cls,
        storage_host: str,
        project_id: PyObjectId,
        blueprint_id: PyObjectId,
        pending_tasks: list[asyncio.Task[None]],
    ):
        cls._sync_conn = ObjectStorageConn(storage_host, project_id, blueprint_id)
        cls._sync_tasks = pending_tasks

    @classmethod
    def clear_sync(cls):
        cls._sync_conn = None
        cls._sync_tasks = None

    def set_obj(self, obj_name: str, obj_type: StorageObjectType, obj_data: bytearray):
        self._obj = StorageObject(name=obj_name, type=obj_type, data=obj_data)

    def set_obj_id(self, obj_id: UUID):
        self._obj_id = obj_id

    def sync_storage(self):
        if self._sync_conn is None or self._sync_tasks is None:
            return

        expected_object_types_dict: dict[str, list[StorageObjectType]] = {
            "Image": [
                StorageObjectType.IMAGE_PNG,
                StorageObjectType.IMAGE_JPEG,
            ],
            "Video": [StorageObjectType.VIDEO_MP4, StorageObjectType.VIDEO_WEBM],
            "Audio": [
                StorageObjectType.AUDIO_MPEG,
                StorageObjectType.AUDIO_WAV,
                StorageObjectType.AUDIO_WEBM,
            ],
            "PDF": [StorageObjectType.PDF],
            "CSV": [StorageObjectType.CSV],
        }
        if self._obj is None and self._obj_id is not None:
            try:
                expected_object_types = expected_object_types_dict[type(self).__name__]

                async def download_task(sync_conn: ObjectStorageConn, id: UUID):
                    obj_name, obj_type, obj_data = await sync_conn.download_object(
                        id, expected_object_types=expected_object_types
                    )
                    self.set_obj(obj_name, obj_type, obj_data)

                self._sync_tasks.append(
                    asyncio.create_task(download_task(self._sync_conn, self._obj_id))
                )
                return
            except KeyError as e:
                raise Exception("Unexpected object type") from e

        if self._obj_id is None and self._obj is not None:

            async def upload_task(sync_conn: ObjectStorageConn, obj: StorageObject):
                self.set_obj_id(
                    await sync_conn.upload_object(obj.name, obj.type, obj.data)
                )

            self._sync_tasks.append(
                asyncio.create_task(upload_task(self._sync_conn, self._obj))
            )
            return

        raise Exception("Unexpected sync state")

    @classmethod
    def serialize_id(cls, value: Self) -> str:
        return f"{value._obj_id}"

    @classmethod
    def serialize_object(cls, value: Self) -> tuple[bytearray, str, str]:
        if value._obj is None:
            raise ValueError("StorageObject serialization error, object not set")
        return (value._obj.data, value._obj.name, value._obj.type)

    def __str__(self) -> str:
        return f"{self._obj_id}"

    def get_name(self):
        if self._obj is None:
            raise Exception("Object is not synced")
        return self._obj.name

    def get_mime_type(self):
        if self._obj is None:
            raise Exception("Object is not synced")
        return self._obj.type

    def get_data(self):
        if self._obj is None:
            raise Exception("Object is not synced")
        return self._obj.data

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: Self,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        json_schema = core_schema.union_schema(
            [
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(
                            cls.validate_from_id
                        ),
                    ]
                ),
                core_schema.chain_schema(
                    [
                        core_schema.uuid_schema(),
                        core_schema.no_info_plain_validator_function(
                            cls.validate_from_id
                        ),
                    ]
                ),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.serialize_id
            ),
        )

        python_schema = core_schema.union_schema(
            [
                json_schema,
                core_schema.no_info_plain_validator_function(cls.validate_from_object),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.serialize_object
            ),
        )
        return core_schema.json_or_python_schema(
            json_schema=json_schema,
            python_schema=python_schema,
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ):
        schema = handler(core_schema.str_schema())
        schema["type"] = cls.__name__.lower()
        return schema


class Image(HykoBaseType):
    MimeTypesUnion = Literal["PNG"] | Literal["JPEG"]

    class MimeType(Enum):
        PNG = "PNG"
        JPEG = "JPEG"

    @staticmethod
    def from_ndarray(
        arr: np.ndarray[Any, Any],
        filename: str = "image.png",
        encoding: MimeTypesUnion = "PNG",
    ) -> "Image":
        file = io.BytesIO()
        img = PIL_Image.fromarray(arr)  # type: ignore
        img.save(file, format="PNG")
        return Image(
            bytearray(file.getbuffer().tobytes()), filename=filename, mime_type=encoding
        )

    @staticmethod
    def from_pil(
        img: PIL_Image.Image,
        filename: str = "image.png",
        encoding: MimeTypesUnion = "PNG",
    ) -> "Image":
        file = io.BytesIO()
        img.save(file, format="PNG")
        return Image(
            bytearray(file.getbuffer().tobytes()), filename=filename, mime_type=encoding
        )

    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, Self],
        filename: Optional[str] = None,
        mime_type: Optional[MimeTypesUnion] = None,
    ) -> None:
        super().__init__(val)

        if isinstance(val, bytearray):
            if filename is None:
                filename = "test.png"

            if mime_type is None:
                mime_type = "PNG"

            if mime_type == "PNG":
                self.set_obj(filename, StorageObjectType.IMAGE_PNG, val)

            elif mime_type == "JPEG":
                self.set_obj(filename, StorageObjectType.IMAGE_JPEG, val)
            else:
                raise ValueError("Got invalid mime type")

            self.sync_storage()
            return

        if self._obj is None and self._obj_id is None:
            raise ValueError(f"Got invalid init value type, {type(val)}")

    @classmethod
    def validate_from_id(cls, value: str | UUID) -> "Image":
        return Image(value)

    @classmethod
    def validate_from_object(
        cls, value: "tuple[bytearray, str, str] | Image"
    ) -> "Image":
        if isinstance(value, Image):
            return value
        if value[2] == StorageObjectType.IMAGE_PNG:
            obj_type = "PNG"
        elif value[2] == StorageObjectType.IMAGE_JPEG:
            obj_type = "JPEG"
        else:
            raise ValueError(f"Invalid StorageObject type, {value[2]}")
        return Image(value[0], value[1], obj_type)

    def to_ndarray(self, keep_alpha_if_png: bool = False) -> NDArray[Any]:
        if self.get_data():
            img_bytes_io = io.BytesIO(self.get_data())
            img = PIL_Image.open(img_bytes_io)
            img = np.asarray(img)
            if keep_alpha_if_png:
                return img
            return img[..., :3]
        else:
            raise RuntimeError("Image decode error (Imagedata not loaded)")

    def to_pil(self, keep_alpha_if_png: bool = False) -> PIL_Image.Image:
        if self.get_data():
            img_bytes_io = io.BytesIO(self.get_data())
            img = PIL_Image.open(img_bytes_io)
            return img
        else:
            raise RuntimeError("Image decode error (Imagedata not loaded)")


class Audio(HykoBaseType):
    MimeTypesUnion = Literal["MPEG"] | Literal["WEBM"] | Literal["WAV"]

    class MimeType(Enum):
        MPEG = "MPEG"
        WEBM = "WEBM"
        WAV = "WAV"

    @staticmethod
    def from_ndarray(arr: np.ndarray[Any, Any], sampling_rate: int) -> "Audio":
        file = io.BytesIO()
        soundfile.write(file, arr, samplerate=sampling_rate, format="MP3")  # type: ignore
        return Audio(
            bytearray(file.getbuffer().tobytes()),
            filename="audio.mp3",
            mime_type="MPEG",
        )

    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, Self],
        filename: Optional[str] = None,
        mime_type: Optional["Audio.MimeTypesUnion"] = None,
    ) -> None:
        super().__init__(val)
        if isinstance(val, bytearray):
            if filename is None:
                filename = "output.mp3"

            if mime_type is None:
                mime_type = "MPEG"

            if mime_type == "MPEG":
                self.set_obj(filename, StorageObjectType.AUDIO_MPEG, val)
            elif mime_type == "WEBM":
                self.set_obj(filename, StorageObjectType.AUDIO_WEBM, val)
            elif mime_type == "WAV":
                self.set_obj(filename, StorageObjectType.AUDIO_WAV, val)
            else:
                raise ValueError(f"Got invalid mime type, {mime_type}")

            self.sync_storage()
            return

        if self._obj is None and self._obj_id is None:
            raise ValueError(f"Got invalid init value type, {type(val)}")

    @classmethod
    def validate_from_id(cls, value: str | UUID) -> "Audio":
        return Audio(value)

    @classmethod
    def validate_from_object(
        cls, value: "tuple[bytearray, str, str] | Audio"
    ) -> "Audio":
        if isinstance(value, Audio):
            return value
        if value[2] == StorageObjectType.AUDIO_MPEG:
            obj_type = "MPEG"
        elif value[2] == StorageObjectType.AUDIO_WEBM:
            obj_type = "WEBM"
        elif value[2] == StorageObjectType.AUDIO_WAV:
            obj_type = "WAV"
        else:
            raise ValueError(f"Invalud StorageObject type, {value[2]}")
        return Audio(value[0], value[1], obj_type)

    _SUBTYPE2DTYPE = {
        "PCM_S8": "int8",
        "PCM_U8": "uint8",
        "PCM_16": "int16",
        "PCM_32": "int32",
        "FLOAT": "float32",
        "DOUBLE": "float64",
    }

    def resample(self, sampling_rate: int):
        if self._obj and self._obj.name:
            with open(self._obj.name, "wb") as f:
                f.write(self.get_data())
            out = "audio_resampled.mp3"
            if self._obj.name == out:
                out = "audio_resampled_2.mp3"

            subprocess.run(
                f"ffmpeg -i {self._obj.name} -ac 1 -ar {sampling_rate} {out} -y".split(
                    " "
                )
            )
            with open(out, "rb") as f:
                self._obj.data = bytearray(f.read())
                self._obj.name = out
            os.remove(out)

    def convert_to(self, new_ext: str):
        if self._obj and self._obj.name:
            # user video.{ext} instead of filename directly to avoid errors with names that has space in it
            _, ext = os.path.splitext(self._obj.name)
            with open(f"/app/video.{ext}", "wb") as f:
                f.write(self.get_data())

            out = "media_converted." + new_ext
            if self._obj.name == out:
                out = "media_converted_2." + new_ext

            subprocess.run(f"ffmpeg -i video.{ext} {out} -y".split(" "))
            with open(out, "rb") as f:
                self._obj.data = bytearray(f.read())
                self._obj.name = out

            os.remove(out)

    def to_ndarray(
        self,
        sampling_rate: Optional[int] = None,
        normalize: bool = True,
        frame_offset: int = 0,
        num_frames: int = -1,
    ) -> Tuple[NDArray[Any], int]:
        if self._obj and self._obj.name:
            self.convert_to("mp3")

            if sampling_rate:
                self.resample(sampling_rate)

            audio_readable = io.BytesIO(self.get_data())
            audio_readable.name = self._obj.name
            with soundfile.SoundFile(audio_readable, "r") as file_:
                if file_.format != "WAV" or normalize:
                    dtype = "float32"
                elif file_.subtype not in Audio._SUBTYPE2DTYPE:
                    raise RuntimeError(f"Unsupported Audio subtype {file_.subtype}")
                else:
                    dtype = Audio._SUBTYPE2DTYPE[file_.subtype]

                frames = file_._prepare_read(frame_offset, None, num_frames)  # type: ignore
                waveform: np.ndarray = file_.read(frames, dtype, always_2d=True)  # type: ignore
                sample_rate: int = file_.samplerate
                return waveform.reshape(waveform.shape[0]), sample_rate  # type: ignore

        else:
            raise RuntimeError("Audio decode error (Audio data not loaded)")


class Video(HykoBaseType):
    MimeTypesUnion = Literal["MP4"] | Literal["WEBM"]

    class MimeType(Enum):
        MP4 = "MP4"
        WEBM = "WEBM"

    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, Self],
        filename: Optional[str] = None,
        mime_type: Optional["Video.MimeTypesUnion"] = None,
    ) -> None:
        super().__init__(val)

        if isinstance(val, bytearray):
            if filename is None:
                filename = "video.mp4"

            if mime_type is None:
                mime_type = "MP4"

            if mime_type == "MP4":
                self.set_obj(filename, StorageObjectType.VIDEO_MP4, val)
            elif mime_type == "WEBM":
                self.set_obj(filename, StorageObjectType.VIDEO_WEBM, val)
            else:
                raise ValueError(f"Got invalid mime type, {mime_type}")

            self.sync_storage()
            return

        if self._obj is None and self._obj_id is None:
            raise ValueError(f"Got invalid init value type, {type(val)}")

    @classmethod
    def validate_from_id(cls, value: str | UUID) -> "Video":
        return Video(value)

    @classmethod
    def validate_from_object(
        cls, value: "tuple[bytearray, str, str] | Video"
    ) -> "Video":
        if isinstance(value, Video):
            return value
        if value[2] == StorageObjectType.VIDEO_MP4:
            obj_type = "MP4"
        elif value[2] == StorageObjectType.VIDEO_WEBM:
            obj_type = "WEBM"
        else:
            raise ValueError(f"Invalid StorageObject type, {value[2]}")
        return Video(value[0], value[1], obj_type)


class PDF(HykoBaseType):
    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, Self],
        filename: Optional[str] = None,
    ) -> None:
        super().__init__(val)
        if isinstance(val, bytearray):
            if filename is None:
                filename = "output.pdf"
            self.set_obj(filename, StorageObjectType.PDF, val)
            self.sync_storage()
            return

        if self._obj is None and self._obj_id is None:
            raise ValueError("Got invalid init value")

    @classmethod
    def validate_from_id(cls, value: str | UUID) -> "PDF":
        return PDF(value)

    @classmethod
    def validate_from_object(cls, value: "tuple[bytearray, str, str] | PDF") -> "PDF":
        if isinstance(value, PDF):
            return value

        if value[2] != StorageObjectType.PDF:
            raise ValueError(f"Invalid StorageObject type, {value[2]}")

        return PDF(value[0], value[1])


class CSV(HykoBaseType):
    def __init__(
        self,
        val: Union[uuid.UUID, bytearray, str, Self],
        filename: Optional[str] = None,
    ) -> None:
        super().__init__(val)
        if isinstance(val, bytearray):
            if filename is None:
                filename = "output.csv"
            self.set_obj(filename, StorageObjectType.CSV, val)
            self.sync_storage()
            return

        if self._obj is None and self._obj_id is None:
            raise ValueError("Got invalid init value")

    @classmethod
    def validate_from_id(cls, value: str | UUID) -> "CSV":
        return CSV(value)

    @classmethod
    def validate_from_object(cls, value: "tuple[bytearray, str, str] | CSV") -> "CSV":
        if isinstance(value, CSV):
            return value

        if value[2] != StorageObjectType.CSV:
            raise ValueError(f"Invalid StorageObject type, {value[2]}")

        return CSV(value[0], value[1])


__all__ = [
    "Image",
    "Audio",
    "Video",
    "PDF",
    "CSV",
]
